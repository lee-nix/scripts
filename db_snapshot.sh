#!/bin/bash --norc
export PATH="/bin:/usr/bin"
BASEDIR="$( cd "$(/usr/bin/dirname "$0")/../../" ; pwd -P )"
. $BASEDIR/etc/site_settings.sh
CURDIR=$( pwd )

error() { printf 'ERROR: %s\n' "$@" 1>&2 ; }

usage() {
  /bin/cat << END
Usage: $0 --action list|snapshot|delete [ --snap-name STR|default ] [ --no-confirm ] [ --no-wait ]

  --action ACTION   REQUIRED. One of "list", "snapshot", or "delete".
                    list     - list all current snapshots for the current lineup.
                    snapshot - create a snapshot with the name specified.
                    delete   - delete the snapshot with the name specified.

  --snap-name STR   Required for "snapshot" and "delete" actions.
                    For "snapshot" action: Name for the snapshot or "default".
                    Default name format: <lineup-name>-manual-snap-<datetime stamp>
                    For "delete" action: Name of snapshot to delete.

  --no-confirm      Don't ask for interactive confirmation.
                    (N/A for "list" action)

  --no-wait         Don't wait for the db snapshot to complete before exiting.
                    (N/A for "list" and "delete" actions)

END
}

# Parse args
SNAP_NAME=""
DO_CONFIRM=1
DO_WAIT=1
DO_LIST=0
DO_SNAP=0
DO_DELETE=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --action|-a)
        ACTION="$2"
        # Set option flags or error if invalid
        if [ "x$ACTION" = "xlist" ]; then
            DO_LIST=1
        elif [ "x$ACTION" = "xsnapshot" ]; then
            DO_SNAP=1
        elif [ "x$ACTION" = "xdelete" ]; then
            DO_DELETE=1
        else
            error "--action '$ACTION' is not valid." ; usage ; exit 1
	    fi;
        shift 2
        ;;
    --snap-name|-n)
        SNAP_NAME="$2"
        # Verify snap-name is not blank
        if [ "x$SNAP_NAME" = "x" ]; then
            error "--snap_name value cannot be blank." ; usage ; exit 1
        fi;
        # Set default snap-name if specified
        if [ "x$SNAP_NAME" = "xdefault" ]; then
            CURDATE=$( /bin/date +%Y%m%d-%H%M )
	        SNAPSHOT_NAME="${LINEUP_NAME}-manual-snap-$CURDATE"
        # Else set user specified snap-name
        else
            SNAPSHOT_NAME="$SNAP_NAME"
        fi;
        shift 2
        ;;
    --no-confirm)
        DO_CONFIRM=0
        shift
        ;;
    --no-wait)
        DO_WAIT=0
        shift
        ;;
    --help|-h)
        usage
        exit 0
        ;;
    *)
        error "Invalid arguments" ; usage ; exit 1
  esac
done

# Verify action is specified
    if [ "x$ACTION" = "x" ]; then
        error "--action is required" ; usage ; exit 1
    fi;

# Verify snap_name specified if action is snapshot
if [ $DO_SNAP -eq 1 ] || [ $DO_DELETE -eq 1 ] && [ "x$SNAP_NAME" = "x" ]; then
    error "--snap-name is required with --action $ACTION." ; usage ; exit 1
fi;

# Wait for db to enter specified state
function wait_for_db {
    TARGET_STATE=$1
    DB_NAME=${2:-${LINEUP_NAME}-traditional-pg}
    # Sleep interval between status checks
    INTERVAL=${3:-10}
    # Timeout for waiting in seconds
    TIMEOUT=${4:-0}
    TIMEOUT_COUNT=0
    _DONE=0
    while [ $_DONE -eq 0 ]; do
        #### TODO when TARGET_STATE is "", suppress errors from this command
        STATE=$( $AWS rds describe-db-instances --db-instance-identifier $DB_NAME 2>/dev/null | jq -r '.DBInstances[0].DBInstanceStatus' )
        DISPLAY_STATE="$STATE"
        if [ "x$TARGET_STATE" = "x" ]; then
            if [ "x$STATE" = "x" ]; then
                DISPLAY_STATE="gone (this is expected)"
            fi
        fi;

        echo "DB instance is currently... $DISPLAY_STATE"

        if [ $TIMEOUT -ne 0 ] && [ $TIMEOUT_COUNT -ge $TIMEOUT ]; then
            error "Wait for DB state: $TARGET_STATE timed out" ; exit 1
        fi;
            
        if [ "$STATE" = "$TARGET_STATE" ]; then
            _DONE=1
        else
            sleep $INTERVAL
            # Increment timeout count if timeout value specified
            if [ $TIMEOUT -ne 0 ]; then
                ((TIMEOUT_COUNT+=INTERVAL))
            fi;
        fi;
    done 
}

# Wait for snapshot complete using aws rds wait command
function wait_for_snapshot_complete {
    # Snapshot ID is same as snapshot name for DB snapshots
    SNAPSHOT_ID=$1
    # Retries if snapshot if rds wait timeout (hard 10 minute timeout)
    RETRIES=${2:-2}
    RETRY_COUNT=0
    _DONE=0
    echo "Waiting for snapshot '${SNAPSHOT_ID}' to complete..."
    while [ $_DONE -eq 0 ]; do
        # Get snapshot percent complete
        SNAPSHOT_PERCENT=$( $AWS rds describe-db-snapshots --db-snapshot-identifier ${SNAPSHOT_ID} --query 'DBSnapshots[0].PercentProgress' )
        echo "${SNAPSHOT_PERCENT}% complete"

        # Call rds wait db-snapshot-completed (hard 10 minute timeout)
        $AWS rds wait db-snapshot-completed --db-snapshot-identifier ${SNAPSHOT_ID}
        RDS_WAIT_EXIT_STATUS=$?

        # Get snapshot percent complete (should be 100% if wait timeout was not hit)
        SNAPSHOT_PERCENT=$( $AWS rds describe-db-snapshots --db-snapshot-identifier ${SNAPSHOT_ID} --query 'DBSnapshots[0].PercentProgress' )
        echo "${SNAPSHOT_PERCENT}% complete"

        # Check for success and retry
        if [ $RDS_WAIT_EXIT_STATUS -eq 0 ]; then
            _DONE=1
        elif [ $RETRY_COUNT -lt $RETRIES ]; then
            ((RETRY_COUNT+=1))
        else
            error "Max retries hit. Your snapshot progress will NOT be affected." ; exit 1
        fi;
    done 
}

# List DB snapshots
if [ $DO_LIST -eq 1 ]; then
    echo "Manual Snapshots"
    echo "----------------"
    $AWS rds describe-db-snapshots --db-instance-identifier ${LINEUP_NAME}-traditional-pg --snapshot-type manual | jq -r '.DBSnapshots | sort_by(.SnapshotCreateTime) | reverse | .[] | .DBSnapshotIdentifier'
    echo ""
    echo "Shared Snapshots"
    echo "----------------"
    $AWS rds describe-db-snapshots --snapshot-type manual | jq -r '.DBSnapshots[] | select(.SourceDBSnapshotIdentifier!="" and .DBInstanceIdentifier!="'${LINEUP_NAME}'-traditional-pg") | .DBSnapshotIdentifier + " (source: " + .DBInstanceIdentifier + ")"'
    echo ""
    echo "Automated Snapshots"
    echo "-------------------"
    $AWS rds describe-db-snapshots --db-instance-identifier ${LINEUP_NAME}-traditional-pg --snapshot-type automated | jq -r '.DBSnapshots | sort_by(.SnapshotCreateTime) | reverse | .[] | .DBSnapshotIdentifier'
fi;

# Take snapshot with specified name
if [ $DO_SNAP -eq 1 ]; then
    # Confirm snapshot
    if [ $DO_CONFIRM -ne 0 ]; then
        echo "Take snapshot of ${LINEUP_NAME}-traditional-pg called: $SNAPSHOT_NAME. Are you sure?"
        read -p "Continue (y/N)? " CONTINUE
        [[ -z "$CONTINUE" || ! "$CONTINUE" =~ ^[yY]$ ]] && exit 0
    fi;
    # Wait for DB to be available
    echo "Waiting for DB to become available before starting snapshot..."
    wait_for_db available ${LINEUP_NAME}-traditional-pg

    # Start DB snapshot
    $AWS rds create-db-snapshot --db-instance-identifier ${LINEUP_NAME}-traditional-pg --db-snapshot-identifier ${SNAPSHOT_NAME} || exit 1

    # Wait for snapshot to finish
    if [ $DO_WAIT -ne 0 ]; then
        ######## Deprecated in favor of aws rds wait db-snapshot-completed command
        # echo "Waiting for snapshot to complete..."
        # First wait for the backup to start for up to 300 seconds
        # Assume something went wrong if it takes longer than that to start the backup
        # wait_for_db backing-up ${LINEUP_NAME}-traditional-pg 10 300
        # Once backup starts, wait for it to complete with no timeout
        # wait_for_db available ${LINEUP_NAME}-traditional-pg
        ########

        # Wait for snapshot to complete
        wait_for_snapshot_complete ${SNAPSHOT_NAME}
    fi;
fi;

# Delete snapshot with specified name
if [ $DO_DELETE -eq 1 ]; then
    # Confirm snapshot
    if [ $DO_CONFIRM -ne 0 ]; then
        echo "DELETE snapshot of ${LINEUP_NAME}-traditional-pg called: $SNAPSHOT_NAME. Are you sure?"
        echo "WARNING: You will NOT be able to undo this action."
        read -p "Continue (y/N)? " CONTINUE
        [[ -z "$CONTINUE" || ! "$CONTINUE" =~ ^[yY]$ ]] && exit 0
    fi;
    
    # Delete DB snapshot
    $AWS rds delete-db-snapshot --db-snapshot-identifier ${SNAPSHOT_NAME} || exit 1
fi;

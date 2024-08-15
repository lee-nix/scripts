#!/bin/bash --norc
export PATH="/bin:/usr/bin"
#BASEDIR="$( cd "$(/usr/bin/dirname "$0")/../" ; pwd -P )"
BASEDIR="$( cd "$(/usr/bin/dirname "$0")/" ; pwd -P )"
. $BASEDIR/etc/site_settings.sh
CURDIR=$( pwd )

TERRAFORM=$BASEDIR/bin/terraform

error() { printf '%s\n' "$@" 1>&2 ; }

usage() {
  /bin/cat << END
Usage: $0 [--no-confirm] 

  --no-confirm       Don't ask for interactive confirmation.

  --no-wait-for-db   Don't wait for the DB to become available before exiting the script

END
}

DO_CONFIRM=1
WAIT_FOR_DB=1
while [[ $# -gt 0 ]]; do
  case "$1" in
    --no-confirm)
        DO_CONFIRM=0
        shift
        ;;
    --no-wait-for-db)
        WAIT_FOR_DB=0
        shift
        ;;
    --help|-h)
        usage
        exit 0
        ;;
    *)
      error "ERROR: Invalid arguments" ; usage ; exit 1
  esac
done

if [ $DO_CONFIRM -ne 0 ]; then
    echo "This will start up jump box and DB for the $LINEUP_NAME lineup. Are you sure?"
    read -p "Continue (y/N)? " CONTINUE
    [[ -z "$CONTINUE" || ! "$CONTINUE" =~ ^[yY]$ ]] && exit 0
fi;

cleanup() {
    /bin/rm -rf $TMP
}
trap cleanup EXIT

TMP=/tmp/partial_unhibernate.$$
/bin/rm -rf $TMP
/bin/mkdir -p $TMP

echo "Turning on the DB"
$AWS rds start-db-instance --db-instance-identifier ${LINEUP_NAME}-traditional-pg

if [ $WAIT_FOR_DB -eq 0 ]; then
    DBSTATUS=$( $AWS rds describe-db-instances --db-instance-identifier ${LINEUP_NAME}-traditional-pg --query 'DBInstances[*].[DBInstanceStatus]' | jq -r '.[0] | .[0]' )
    while [ ! "$DBSTATUS" = "available" ]; do
        date +"[%H:%M:%S] Waiting for DB Instance to be available... Current Status is: $DBSTATUS"
        sleep 30
        DBSTATUS=$( $AWS rds describe-db-instances --db-instance-identifier ${LINEUP_NAME}-traditional-pg --query 'DBInstances[*].[DBInstanceStatus]' | jq -r '.[0] | .[0]' )
    done
fi;

echo "Reactivating the jump box"
$AWS autoscaling resume-processes --auto-scaling-group-name ${LINEUP_NAME}-jump-auto-scaling --scaling-processes "Launch" "ReplaceUnhealthy"


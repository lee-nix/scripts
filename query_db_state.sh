#!/bin/bash --norc
export PATH="/bin:/usr/bin"
#BASEDIR="$( cd "$(/usr/bin/dirname "$0")/../" ; pwd -P )"
BASEDIR="$( cd "$(/usr/bin/dirname "$0")/" ; pwd -P )"
. $BASEDIR/etc/site_settings.sh
CURDIR=$( pwd )

TERRAFORM=$BASEDIR/bin/terraform



DBSTATUS=$( $AWS rds describe-db-instances --db-instance-identifier ${LINEUP_NAME}-traditional-pg --query 'DBInstances[*].[DBInstanceStatus]' | jq -r '.[0] | .[0]' )
while [[ ! "$DBSTATUS" =~ 'available' ]]; do
    date +"[%H:%M:%S] Waiting for DB Instance to be available... Current Status is: $DBSTATUS"
    sleep 30
    DBSTATUS=$( $AWS rds describe-db-instances --db-instance-identifier ${LINEUP_NAME}-traditional-pg --query 'DBInstances[*].[DBInstanceStatus]' | jq -r '.[0] | .[0]' )
done
echo "DB is now available"
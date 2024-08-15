#!/bin/bash
. /home/terraform/etc/site_settings.sh

#TABLE_NAME="perfman_users"
cleanup() {
	/bin/rm -rf $TMP
}
trap cleanup EXIT


#ALL_TABLES="perfman_accounts perfman_lineups perfman_sync_items perfman_themes perfman_users"
ALL_TABLES="$( aws dynamodb list-tables --output text --query "TableNames[?contains(@, 'VirusTotal-Cache') == \`false\`]" )"
#ALL_TABLES="perfman_sync_items"
for TABLE_NAME in $ALL_TABLES; do

	TMP=/tmp/dynamodb_delete.$$
	/bin/rm -rf $TMP
	/bin/mkdir -p $TMP

	PRIMARY_KEY=$( aws dynamodb describe-table --table-name ${TABLE_NAME} | jq '.Table.AttributeDefinitions[0]' )
	PRIMARY_KEY_NAME=$( echo $PRIMARY_KEY | jq -r '.AttributeName' )
	echo $PRIMARY_KEY_NAME

	DELETE_COUNT=1
	while [ $DELETE_COUNT -ne 0 ]; do
		aws dynamodb scan --table-name ${TABLE_NAME} --projection-expression "${PRIMARY_KEY_NAME}" --max-items 25 | jq '.Items[] | { "DeleteRequest": { "Key": . } }' | jq -s '{ "'${TABLE_NAME}'": . }' > $TMP/delete_request.json

		DELETE_COUNT=$( cat $TMP/delete_request.json | jq '.'${TABLE_NAME}' | length' )

		if [ $DELETE_COUNT -gt 0 ]; then
			aws dynamodb batch-write-item --request-items file://$TMP/delete_request.json --return-consumed-capacity TOTAL
		fi;
	done

done


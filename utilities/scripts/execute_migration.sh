#!/bin/bash

LOG_FILE="/app/utilities/scripts/execute_migrations.log"

echo enter to file >> "$LOG_FILE"

source /app/.env

if  [[ -z "${MYSQL_ROOT_PASSWORD}" ]] &&
    [[ -z "${MYSQL_DATABASE}" ]] &&
    [[ -z "${MYSQL_USER}" ]] &&
    [[ -z "${MYSQL_PASSWORD}" ]]; then

    echo The variables does not exist >> "$LOG_FILE"
    exit 1 

else
  MYSQL_ROOT_PASSWORD="${MYSQL_ROOT_PASSWORD}"
  MYSQL_DATABASE="${MYSQL_DATABASE}"
  MYSQL_USER="${MYSQL_USER}"
  MYSQL_PASSWORD="${MYSQL_PASSWORD}"
  MYSQL_HOST="${MYSQL_HOST}"
fi

set -x
result=$(mysql -h "$MYSQL_HOST" -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" -D "$MYSQL_DATABASE" -e "show tables")
set +x

if [[ -z "${result}" ]]; then
    flask db upgrade
    echo "The migrations are ready." >> "$LOG_FILE"
else
    echo "There are existing migrations in the database." >> "$LOG_FILE"
fi

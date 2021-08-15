#!/bin/bash

set -e

if [ "$1" = 'webserver' ]; then
    airflow db init
    airflow users create --username admin --firstname Michael --lastname Graf --role Admin --email admin@station.org -p admin
    airflow scheduler &
    exec  airflow webserver

elif [ "$1" = 'worker' ]; then
    exec  airflow worker

elif [ "$1" = 'init' ]; then
    airflow db init
    airflow users create --username admin --firstname FIRST_NAME --lastname LAST_NAME --role Admin --email admin@example.org -p admin
    airflow connections add 'postgres_db' --conn-type 'postgres' --conn-login 'admin' --conn-password 'admin' --conn-host 'postgres' --conn-port '5432' --conn-schema "pht_station_${STATION_ID}"
    # exec  station_airflow worker
else
    exec "$@"
fi
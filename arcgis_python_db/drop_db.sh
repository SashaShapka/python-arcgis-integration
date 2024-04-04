#!/bin/bash


# Drop Postgres Database with PSQL

# Variables
db_name="$1"
db_user="$2"
password="$3"



export PGPASSWORD='password'

# Drop Database

psql -U postgres -c "DROP DATABASE $db_name;"

psql -U postgres -c "REASSIGN OWNED BY $db_user TO postgres;"

psql -U postgres -c "DROP OWNED BY $db_user;"

psql -U postgres -c "DROP ROLE $db_user;"

echo "Database $db_name dropped with user $db_user and password $password"
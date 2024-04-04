#!/bin/bash



# Create Postgres Database with PSQL

# Variables
db_name="$1"
db_user="$2"
password="$3"
host="$4"
port="$5"


export PGPASSWORD='password'

# Create Database
psql -U postgres -h $host -p $port -c "CREATE DATABASE $db_name;"

# Create User
psql -U postgres -h $host -p $port -c "CREATE USER $db_user WITH PASSWORD '$password';"

# Grant Permissions
psql -U postgres -h $host -p $port -c "GRANT ALL PRIVILEGES ON DATABASE $db_name TO $db_user;"

echo "Database $db_name created with user $db_user and password $password"
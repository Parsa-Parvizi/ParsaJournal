#!/bin/bash
# Simple PostgreSQL Setup for Parsa Journal

set -e

echo "Setting up PostgreSQL database..."

# Read database credentials from .env
if [ -f .env ]; then
    DB_NAME=$(grep "^DB_NAME=" .env | cut -d '=' -f2 | tr -d ' ' || echo "parsajournal_db")
    DB_USER=$(grep "^DB_USER=" .env | cut -d '=' -f2 | tr -d ' ' || echo "postgres")
    DB_PASSWORD=$(grep "^DB_PASSWORD=" .env | cut -d '=' -f2 | tr -d ' ' || echo "postgres")
else
    DB_NAME="parsajournal_db"
    DB_USER="postgres"
    DB_PASSWORD="postgres"
fi

echo "Database: $DB_NAME"
echo "User: $DB_USER"

# Connect as postgres superuser and setup
sudo -u postgres psql <<EOF
-- Create database if not exists
SELECT 'CREATE DATABASE $DB_NAME' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '$DB_NAME')\gexec

-- Set password for postgres user
ALTER USER $DB_USER WITH PASSWORD '$DB_PASSWORD';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;

-- Set database settings
ALTER DATABASE $DB_NAME SET timezone TO 'Asia/Tehran';
EOF

echo "Database setup complete!"
echo "Now you can run: python manage.py migrate"


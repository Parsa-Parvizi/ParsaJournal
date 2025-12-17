#!/bin/bash
# Setup PostgreSQL Database for Parsa Journal

set -e

echo "=========================================="
echo "Parsa Journal - Database Setup"
echo "=========================================="

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
else
    echo "Error: .env file not found!"
    echo "Please create .env file from .env.example"
    exit 1
fi

DB_NAME=${DB_NAME:-parsajournal_db}
DB_USER=${DB_USER:-postgres}
DB_PASSWORD=${DB_PASSWORD:-postgres}
DB_HOST=${DB_HOST:-localhost}
DB_PORT=${DB_PORT:-5432}

echo "Database Configuration:"
echo "  Name: $DB_NAME"
echo "  User: $DB_USER"
echo "  Host: $DB_HOST"
echo "  Port: $DB_PORT"
echo ""

# Check if PostgreSQL is running
echo "Checking PostgreSQL service..."
if ! sudo systemctl is-active --quiet postgresql; then
    echo "PostgreSQL is not running. Starting PostgreSQL..."
    sudo systemctl start postgresql
    sleep 2
fi

# Create database and user
echo "Creating database and user..."
sudo -u postgres psql <<EOF
-- Create database
SELECT 'CREATE DATABASE $DB_NAME' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '$DB_NAME')\gexec

-- Create user if not exists
DO \$\$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_user WHERE usename = '$DB_USER') THEN
        CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';
    END IF;
END
\$\$;

-- Grant privileges
ALTER DATABASE $DB_NAME OWNER TO $DB_USER;
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;

-- Set client encoding
ALTER DATABASE $DB_NAME SET client_encoding TO 'utf8';
ALTER DATABASE $DB_NAME SET default_transaction_isolation TO 'read committed';
ALTER DATABASE $DB_NAME SET timezone TO 'Asia/Tehran';
EOF

echo "Database created successfully!"
echo ""

# Test database connection
echo "Testing database connection..."
export PGPASSWORD=$DB_PASSWORD
if psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "SELECT version();" > /dev/null 2>&1; then
    echo "Database connection successful!"
else
    echo "Error: Could not connect to database!"
    exit 1
fi

echo ""
echo "=========================================="
echo "Database setup completed!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Run migrations: python manage.py migrate"
echo "2. Create superuser: python manage.py createsuperuser"
echo "3. Start server: python manage.py runserver"
echo ""


#!/bin/bash
# Fix Database Connection for Parsa Journal

set -e

echo "=========================================="
echo "Fixing PostgreSQL Database Connection"
echo "=========================================="

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
else
    echo "Error: .env file not found!"
    exit 1
fi

DB_NAME=${DB_NAME:-parsajournal_db}
DB_USER=${DB_USER:-postgres}
DB_PASSWORD=${DB_PASSWORD:-postgres}

echo "Database Configuration:"
echo "  Name: $DB_NAME"
echo "  User: $DB_USER"
echo ""

# Check if we can connect as postgres user
echo "Checking PostgreSQL connection..."
if sudo -u postgres psql -c "SELECT 1;" > /dev/null 2>&1; then
    echo "✓ Can connect to PostgreSQL as postgres user"
else
    echo "✗ Cannot connect to PostgreSQL"
    echo "Please check PostgreSQL installation and service status"
    exit 1
fi

# Check if database exists
echo "Checking if database exists..."
if sudo -u postgres psql -lqt | cut -d \| -f 1 | grep -qw "$DB_NAME"; then
    echo "✓ Database '$DB_NAME' exists"
else
    echo "Creating database '$DB_NAME'..."
    sudo -u postgres psql <<EOF
CREATE DATABASE $DB_NAME;
EOF
    echo "✓ Database created"
fi

# Check if user exists and set password
echo "Setting up database user..."
sudo -u postgres psql <<EOF
-- Create user if not exists
DO \$\$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_user WHERE usename = '$DB_USER') THEN
        CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';
    ELSE
        ALTER USER $DB_USER WITH PASSWORD '$DB_PASSWORD';
    END IF;
END
\$\$;

-- Grant privileges
ALTER DATABASE $DB_NAME OWNER TO $DB_USER;
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;

-- Set database settings
ALTER DATABASE $DB_NAME SET client_encoding TO 'utf8';
ALTER DATABASE $DB_NAME SET default_transaction_isolation TO 'read committed';
ALTER DATABASE $DB_NAME SET timezone TO 'Asia/Tehran';
EOF

echo "✓ User configured"

# Test connection with password
echo "Testing database connection..."
export PGPASSWORD=$DB_PASSWORD
if psql -h localhost -U $DB_USER -d $DB_NAME -c "SELECT version();" > /dev/null 2>&1; then
    echo "✓ Database connection successful!"
else
    echo "✗ Database connection failed"
    echo ""
    echo "Trying to fix authentication..."
    
    # Update pg_hba.conf to allow password authentication
    PG_HBA_CONF=$(sudo -u postgres psql -t -P format=unaligned -c 'SHOW hba_file;' | xargs)
    if [ -f "$PG_HBA_CONF" ]; then
        echo "Updating pg_hba.conf..."
        # Backup original
        sudo cp "$PG_HBA_CONF" "${PG_HBA_CONF}.backup"
        
        # Add local connection with md5 authentication if not exists
        if ! grep -q "local.*all.*all.*md5" "$PG_HBA_CONF"; then
            echo "local   all             all                                     md5" | sudo tee -a "$PG_HBA_CONF"
        fi
        if ! grep -q "host.*all.*all.*127.0.0.1/32.*md5" "$PG_HBA_CONF"; then
            echo "host    all             all             127.0.0.1/32            md5" | sudo tee -a "$PG_HBA_CONF"
        fi
        if ! grep -q "host.*all.*all.*::1/128.*md5" "$PG_HBA_CONF"; then
            echo "host    all             all             ::1/128                 md5" | sudo tee -a "$PG_HBA_CONF"
        fi
        
        # Reload PostgreSQL
        echo "Reloading PostgreSQL configuration..."
        sudo systemctl reload postgresql 2>/dev/null || sudo -u postgres pg_ctl reload -D /var/lib/postgresql/*/main 2>/dev/null || echo "Please restart PostgreSQL manually"
        
        sleep 2
        
        # Test again
        if psql -h localhost -U $DB_USER -d $DB_NAME -c "SELECT version();" > /dev/null 2>&1; then
            echo "✓ Database connection successful after fixing authentication!"
        else
            echo "✗ Still having connection issues"
            echo "Please check:"
            echo "1. PostgreSQL is running: sudo systemctl status postgresql"
            echo "2. Password in .env file matches PostgreSQL user password"
            echo "3. pg_hba.conf allows local connections"
            exit 1
        fi
    fi
fi

echo ""
echo "=========================================="
echo "Database setup completed!"
echo "=========================================="
echo ""
echo "You can now run:"
echo "  python manage.py migrate"
echo "  python manage.py createsuperuser"
echo "  python manage.py runserver"
echo ""


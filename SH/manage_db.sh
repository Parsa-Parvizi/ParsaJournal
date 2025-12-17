#!/bin/bash
# Database Management Script for Parsa Journal

set -e

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
DB_HOST=${DB_HOST:-localhost}
DB_PORT=${DB_PORT:-5432}

export PGPASSWORD=$DB_PASSWORD

case "$1" in
    start)
        echo "Starting PostgreSQL..."
        sudo systemctl start postgresql
        ;;
    stop)
        echo "Stopping PostgreSQL..."
        sudo systemctl stop postgresql
        ;;
    status)
        echo "PostgreSQL Status:"
        sudo systemctl status postgresql
        ;;
    migrate)
        echo "Running migrations..."
        source venv/bin/activate
        python manage.py makemigrations
        python manage.py migrate
        ;;
    createsuperuser)
        echo "Creating superuser..."
        source venv/bin/activate
        python manage.py createsuperuser
        ;;
    shell)
        echo "Opening database shell..."
        psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME
        ;;
    backup)
        echo "Backing up database..."
        BACKUP_FILE="backup_$(date +%Y%m%d_%H%M%S).sql"
        pg_dump -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME > $BACKUP_FILE
        echo "Backup saved to: $BACKUP_FILE"
        ;;
    restore)
        if [ -z "$2" ]; then
            echo "Usage: $0 restore <backup_file.sql>"
            exit 1
        fi
        echo "Restoring database from $2..."
        psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME < "$2"
        echo "Database restored!"
        ;;
    *)
        echo "Usage: $0 {start|stop|status|migrate|createsuperuser|shell|backup|restore}"
        echo ""
        echo "Commands:"
        echo "  start           - Start PostgreSQL service"
        echo "  stop            - Stop PostgreSQL service"
        echo "  status          - Check PostgreSQL status"
        echo "  migrate         - Run database migrations"
        echo "  createsuperuser - Create Django superuser"
        echo "  shell           - Open PostgreSQL shell"
        echo "  backup          - Backup database"
        echo "  restore <file>  - Restore database from backup"
        exit 1
        ;;
esac


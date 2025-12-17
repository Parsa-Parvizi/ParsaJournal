#!/bin/bash
# Quick Start Script for Parsa Journal

set -e

echo "=========================================="
echo "Parsa Journal - Quick Start"
echo "=========================================="

# Check if .env exists
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "Please edit .env file and update configuration values."
    else
        echo "Error: .env.example not found!"
        exit 1
    fi
fi

# Activate virtual environment
if [ -d venv ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
else
    echo "Error: Virtual environment not found!"
    echo "Please create virtual environment: python3 -m venv venv"
    exit 1
fi

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Check PostgreSQL
echo "Checking PostgreSQL..."
if sudo systemctl is-active --quiet postgresql; then
    echo "PostgreSQL is running."
else
    echo "PostgreSQL is not running. Starting PostgreSQL..."
    sudo systemctl start postgresql
    sleep 2
fi

# Setup database
echo "Setting up database..."
if [ -f setup_database.sh ]; then
    bash setup_database.sh
else
    echo "Warning: setup_database.sh not found. Skipping database setup."
fi

# Run migrations
echo "Running migrations..."
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
echo ""
read -p "Do you want to create a superuser? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python manage.py createsuperuser
fi

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo ""
echo "=========================================="
echo "Setup completed!"
echo "=========================================="
echo ""
echo "To start the server:"
echo "  python manage.py runserver"
echo ""
echo "To access admin panel:"
echo "  http://localhost:8000/admin"
echo ""


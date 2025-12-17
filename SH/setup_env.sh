#!/bin/bash
# Setup script to create .env file from .env.example

if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo ".env file created successfully!"
    echo "Please edit .env file and update the configuration values."
else
    echo ".env file already exists. Skipping..."
fi

# Create logs directory
mkdir -p logs
echo "Logs directory created."

# Create media and static directories
mkdir -p media staticfiles
echo "Media and static directories created."

echo "Setup complete!"


#!/bin/bash

# Azure App Service startup script
# This script is automatically executed when the container starts

echo "Starting Teams AddBot..."

# Install dependencies if needed
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Start the application with Gunicorn
echo "Starting application with Gunicorn..."
exec gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 --access-logfile - --error-logfile - app:app

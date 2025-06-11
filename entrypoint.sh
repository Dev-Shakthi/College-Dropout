#!/bin/bash
set -e

echo "Starting entrypoint script..."

if [ ! -z "$APP_ZIP_URL" ]; then
    echo "Downloading app from $APP_ZIP_URL"
    wget -O /app/app.zip "$APP_ZIP_URL"
    unzip -o /app/app.zip -d /app/
    
    if [ -d "/app/College Dropout" ]; then
        echo "Flattening folder structure from 'College Dropout/'..."
        mv /app/College\ Dropout/* /app/
        rm -rf /app/College\ Dropout/
    fi
    
    rm -f /app/app.zip
fi

if [ ! -f /app/app.py ]; then
    echo "Error: /app/app.py not found. Exiting."
    exit 1
fi

if [ ! -f /app/file_manager.py ]; then
    echo "Error: /app/file_manager.py not found. Exiting."
    exit 1
fi

echo "Starting supervisor..."
exec supervisord -c /etc/supervisor/conf.d/supervisord.conf

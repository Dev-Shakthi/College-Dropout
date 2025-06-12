#!/bin/bash
set -e

echo "Starting entrypoint script..."

# Download and unzip the app
if [ ! -z "$APP_ZIP_URL" ]; then
    echo "Downloading app from $APP_ZIP_URL"
    wget -O /app/app.zip "$APP_ZIP_URL"
    unzip -o /app/app.zip -d /app/
    rm -f /app/app.zip
fi

# Check required files
if [ ! -f /app/app.py ]; then
    echo "Error: /app/app.py not found. Exiting."
    ls /app
    exit 1
fi

if [ ! -f /app/file_manager.py ]; then
    echo "Error: /app/file_manager.py not found. Exiting."
    exit 1
fi

mkdir -p /var/log/nginx /var/run /var/log/supervisor

echo "Starting supervisor..."
exec supervisord -c /etc/supervisor/conf.d/supervisord.conf

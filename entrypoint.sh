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

# Wait a moment for files to be ready
sleep 2

echo "Starting supervisor..."
exec supervisord -c /etc/supervisor/conf.d/supervisord.conf

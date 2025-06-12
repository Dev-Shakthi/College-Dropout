#!/bin/bash
set -e

echo "Starting entrypoint script..."
echo "Current user: $(whoami)"
echo "Current UID: $(id -u)"
echo "Current GID: $(id -g)"

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

# Create required directories with proper permissions
echo "Creating directories and setting permissions..."
mkdir -p /var/log/nginx /var/run /var/log/supervisor
chmod 755 /var/log/nginx /var/run /var/log/supervisor

# Test nginx config
echo "Testing nginx configuration..."
nginx -t -c /app/nginx.conf 2>&1 || echo "Nginx test failed with above error"

# Test if we can write to pidfile location
echo "Testing pidfile write access..."
touch /var/run/supervisord.pid 2>&1 || echo "Cannot write to /var/run/supervisord.pid"

# Start nginx manually to see the error
echo "Testing nginx start manually..."
nginx -c /app/nginx.conf 2>&1 || echo "Manual nginx start failed with above error"

echo "Starting supervisor..."
exec supervisord -c /etc/supervisor/conf.d/supervisord.conf

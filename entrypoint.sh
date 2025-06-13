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

# Skip nginx entirely for now - just run FastAPI and Streamlit directly
echo "Starting FastAPI..."
uvicorn file_manager:app --host 0.0.0.0 --port 80 

# Keep container alive
wait

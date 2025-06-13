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

echo "Starting Streamlit on port 80..."  
streamlit run app.py --server.address=0.0.0.0 --server.port=80 &

echo "Starting FastAPI on port 8000..."
uvicorn file_manager:app --host 0.0.0.0 --port 8000 &

# Keep container alive
wait

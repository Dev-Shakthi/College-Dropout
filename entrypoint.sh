#!/bin/bash

set -e  # Exit on any error

if [ ! -z "$APP_ZIP_URL" ]; then
  echo "Downloading app from $APP_ZIP_URL"
  wget -O /app/app.zip "$APP_ZIP_URL"

  echo "Unzipping downloaded app..."
  unzip -o /app/app.zip -d /app/

  # If the app is nested inside a folder (e.g., 'College Dropout'), move files up
  if [ -d "/app/College Dropout" ]; then
    echo "Flattening folder structure from 'College Dropout/'..."
    mv /app/College\ Dropout/* /app/
    rm -rf /app/College\ Dropout/
  fi
fi

# Check if app.py exists
if [ ! -f /app/app.py ]; then
  echo "❌ Error: /app/app.py not found. Exiting."
  exit 1
fi

# Start the Streamlit app
echo "✅ Starting Streamlit app..."
exec streamlit run /app/app.py --server.address=0.0.0.0 --server.port=8501

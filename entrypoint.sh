set -e

if [ ! -z "$APP_ZIP_URL" ]; then
  echo "Downloading app from $APP_ZIP_URL"
  wget -O /app/app.zip "$APP_ZIP_URL"
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
  echo "Error: /app/app.py not found. Exiting."
  exit 1
fi

#Start FastAPI in background
echo "Starting FastAPI file manager on port 8000..."
uvicorn file_manager:app --host 0.0.0.0 --port 8000 &

#Start Streamlit app
echo "Starting Streamlit app on port 8501..."
exec streamlit run /app/app.py --server.address=0.0.0.0 --server.port=8501

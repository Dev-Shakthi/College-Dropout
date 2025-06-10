#!/bin/bash

# Optional zip download step
if [ ! -z "$APP_ZIP_URL" ]; then
  echo "Downloading app from $APP_ZIP_URL"
  wget "$APP_ZIP_URL" -O /app/app.zip
  unzip -o /app/app.zip -d /app/
fi

# Run Streamlit app
exec streamlit run /app/app.py --server.address=0.0.0.0 --server.port=8501

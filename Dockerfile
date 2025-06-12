FROM python:3-slim

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV APP_HOME=/app

WORKDIR $APP_HOME

# Install system dependencies including nginx and supervisor
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    nginx \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Install Python requirements
COPY requirements.txt . 
RUN python -m pip install --no-cache-dir --root-user-action=ignore -r requirements.txt

# Copy configuration files
COPY nginx.conf /etc/nginx/nginx.conf
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Add the custom entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Create non-root user and set permissions
RUN adduser -u 5678 --disabled-password --gecos "" appuser && \
    chown -R appuser $APP_HOME && \
    mkdir -p /var/log/supervisor && \
    chown -R appuser /var/log/supervisor && \
    chown -R appuser /var/log/nginx

USER appuser

# Expose ports for nginx, streamlit, fastapi
EXPOSE 80 8501 8000

ENTRYPOINT ["/entrypoint.sh"]

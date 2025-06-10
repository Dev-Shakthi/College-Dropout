FROM python:3-slim

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV APP_HOME=/app
WORKDIR $APP_HOME

# Install requirements
COPY requirements.txt .
RUN python -m pip install --upgrade pip && \
    python -m pip install -r requirements.txt

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Create non-root user and give permissions
RUN adduser -u 5678 --disabled-password --gecos "" appuser && \
    chown -R appuser $APP_HOME
USER appuser

# Expose Streamlit port
EXPOSE 8501

# Start container using custom entrypoint
ENTRYPOINT ["/entrypoint.sh"]

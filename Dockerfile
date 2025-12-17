FROM python:3.12-slim

WORKDIR /app

# Install system dependencies if needed (e.g. for potential future needs)
# RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .

# Install dependencies
RUN pip install --no-cache-dir .

# Copy application code
COPY . .

# Default command (overridden in docker-compose)
CMD ["python", "app/app.py"]

FROM python:3.12-slim

WORKDIR /app

# Install system dependencies including LaTeX
RUN apt-get update && apt-get install -y \
    texlive-latex-base \
    texlive-fonts-recommended \
    texlive-latex-extra \
    texlive-fonts-extra \
    texlive-lang-cyrillic \
    cm-super \
    && rm -rf /var/lib/apt/lists/*
# RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .

# Install dependencies
RUN pip install --no-cache-dir .

# Copy application code
COPY . .

# Default command (overridden in docker-compose)
CMD ["python", "app/app.py"]

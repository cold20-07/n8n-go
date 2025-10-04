# Multi-stage Dockerfile for n8n Workflow Generator

# Stage 1: Build TypeScript
FROM node:18-alpine AS typescript-builder

WORKDIR /app

# Copy package files
COPY package*.json ./
COPY tsconfig.json ./

# Install dependencies
RUN npm ci --only=development

# Copy TypeScript source
COPY main.ts ./

# Build TypeScript
RUN npm run build

# Stage 2: Python Flask Application
FROM python:3.11-slim AS python-app

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy Python requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Python application files
COPY app.py .
COPY run.py .
COPY n8n_workflow_research.py .
COPY enhance_workflow_output.py .

# Copy built TypeScript files from previous stage
COPY --from=typescript-builder /app/dist ./static/js/

# Stage 3: Final production image
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies
COPY --from=python-app /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=python-app /usr/local/bin /usr/local/bin

# Copy application files
COPY --from=python-app /app .

# Copy static files
COPY templates ./templates
COPY static ./static

# Create non-root user
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app

USER app

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/ || exit 1

# Run the application
CMD ["python", "run.py"]
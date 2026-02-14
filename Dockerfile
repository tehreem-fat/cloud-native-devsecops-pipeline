# ===========================
# Stage 1: Build Stage
# ===========================
FROM python:3.11-slim AS build

# Set working directory
WORKDIR /app

# Copy requirements first for caching
COPY app/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source code
COPY app/ /app/

# ===========================
# Stage 2: Production Stage
# ===========================
FROM python:3.11-slim

# Install curl (for healthcheck) and clean apt cache
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd -m appuser

# Set working directory
WORKDIR /app

# Copy dependencies and app from build stage
COPY --from=build /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=build /app /app

# Give ownership to non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 5000

# Healthcheck for container
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s \
  CMD curl -f http://localhost:5000/health || exit 1

# Run the Flask app
CMD ["python3", "app.py"]

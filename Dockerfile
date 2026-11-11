# Multi-stage or lightweight production container for FV-SEC001 Aggregator
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code and entrypoint
COPY src/ ./src/
COPY aggregator.py .

# Mount volume for inputs/outputs
VOLUME ["/app/data", "/app/results"]

# Default entrypoint
ENTRYPOINT ["python", "aggregator.py"]
CMD ["--input", "ad_data.csv", "--output", "results/"]

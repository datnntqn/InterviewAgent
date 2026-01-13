FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY ai/requirements.txt /app/ai/requirements.txt
COPY service/requirements.txt /app/service/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/ai/requirements.txt
RUN pip install --no-cache-dir -r /app/service/requirements.txt

# Copy source code
COPY ai/src /app/ai/src
COPY service/src /app/service/src

# Set Python path
ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["uvicorn", "service.src.api:app", "--host", "0.0.0.0", "--port", "8000"]

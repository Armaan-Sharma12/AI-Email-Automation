# Use official Python 3.10 slim image
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements file first for caching layers
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Default command when container runs
CMD ["python", "main.py"]

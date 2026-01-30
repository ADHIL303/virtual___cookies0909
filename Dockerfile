# Simple Dockerfile for Flask Portfolio App
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=main.py

# Install pip upgrade
RUN pip install --no-cache-dir --upgrade pip

# Set working directory
WORKDIR /app

# Copy entire project (all files and folders except venv via .dockerignore)
COPY . .

# Install Python requirements
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 5000

# Run main.py
CMD ["python", "main.py"]

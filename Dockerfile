# Use official Python base image
FROM python:3.11-slim

# Set workdir
WORKDIR /app

# Copy files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8080

# Start the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
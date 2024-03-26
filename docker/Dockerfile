# Use a lightweight Python base image
FROM python:3.9-slim

# Set a working directory for the application
WORKDIR /app

# Copy requirements.txt
COPY requirements.txt ./

# Install dependencies
RUN pip install -r requirements.txt

# Expose port 80 for the web service
EXPOSE 80

# Set the command to run the application
CMD ["python", "counter-service.py"]

# Use a lightweight Python base image
FROM python:3.9-slim

# Set a working directory for the application
WORKDIR /app

# Copy requirements.txt (if you have one)
COPY requirements.txt ./

# Install dependencies (if using requirements.txt)
RUN pip install -r requirements.txt

# Copy the application code
COPY . .

# Expose port 80 for the web service
EXPOSE 80

# Set the command to run the application
CMD ["python", "counter_service.py"]

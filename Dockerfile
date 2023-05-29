# Use a Python base image
FROM python:3.9-slim-buster

# Install dependencies
RUN pip install boto3

# Copy the Python script into the container
COPY server.py /app/server.py

# Set the working directory
WORKDIR /app

# Expose the server port
EXPOSE 8000

# Run the Python script
CMD ["python", "server.py"]

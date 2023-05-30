# Use a Python base image
FROM python:3.11-slim-buster

LABEL org.opencontainers.image.source https://github.comajacobfg/list-aws-params/
LABEL org.opencontainers.image.description "container image retriving aws params"
LABEL org.opencontainers.image.licenses MIT

# Install dependencies
RUN pip install boto3

# Copy the Python script into the container
COPY server.py /app/server.py

# Set the working directory
WORKDIR /app

# Expose the server port
EXPOSE 8000

# Required
ENV AWS_DEFAULT_REGION ap-southeast-2

# Run the Python script
CMD ["python", "server.py"]

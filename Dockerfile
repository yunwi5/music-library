# Use the official Python image as the base image
FROM python:3.10-alpine

# Set the working directory in the container to /app
WORKDIR /app

# Copy requirements.txt file first
COPY requirements.txt requirements.txt

# Install the required packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Set the environment variable for Flask
ENV FLASK_APP=wsgi.py

# Expose port 5000 for Gunicorn to listen on
EXPOSE 5000

# Command to run the Flask application
CMD [ "gunicorn", "wsgi:app", "-b", "0.0.0.0:5000"]

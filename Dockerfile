# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Install system dependencies required for Tkinter and MySQL
RUN apt-get update && apt-get install -y \
    python3-tk \
    tk \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Define environment variable
ENV DISPLAY=:0

# Run the application
CMD ["python", "Inventario.py"]

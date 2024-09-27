# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Install necessary system packages
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    tesseract-ocr \
    libtesseract-dev \
    libleptonica-dev \
    ffmpeg \
    curl \
    && apt-get clean

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8080 (if needed, adjust based on your app)
EXPOSE 8080

# Set environment variable
ENV NAME Bot

# Run the bot
CMD ["python", "bot.py"]

# Use the official Python image as a base
FROM python:3.9-slim

# Prevent Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

# Update and install necessary system packages, including Tesseract and Hindi language data
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-hin \
    libtesseract-dev \
    ffmpeg \
    libsm6 \
    libxext6 \
    wget && \
    rm -rf /var/lib/apt/lists/*

# Set the TESSDATA_PREFIX environment variable
ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/5/tessdata/

# Create a working directory
WORKDIR /app

# Copy and install requirements
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app/

# Set the PORT environment variable for Azure
ENV PORT=8000
EXPOSE 8000

# Command to run your bot
CMD ["python", "your_script.py"]

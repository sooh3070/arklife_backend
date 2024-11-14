# Base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install Chrome, ChromeDriver, and dependencies
RUN apt-get update && apt-get install -y \
    libnss3 libx11-xcb1 libxcomposite1 libxcursor1 \
    libxi6 libxrandr2 libxss1 libatk-bridge2.0-0 libgtk-3-0 \
    chromium chromium-driver && apt-get clean

# Ensure /app/.wdm exists and is writable
RUN mkdir -p /app/.wdm && chmod -R 777 /app/.wdm

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Command to run FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-pyqt5 \
    libgl1-mesa-glx \
    i2c-tools \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set environment variable for QT
ENV QT_QPA_PLATFORM=xcb
ENV PYTHONPATH=/app/src

# Command to run the application
CMD ["python", "src/app.py"]
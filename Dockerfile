# Dockerfile

FROM python:3.9-slim

# Create a directory
WORKDIR /app

# Copy requirements
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy your Python scripts
COPY data_processing.py /app/
COPY train_prophet.py /app/
COPY predict_prophet.py /app/
COPY sales.csv /app/          
# Optionally create a models/ directory if you like
# RUN mkdir /app/models

# No default CMD because Argo will override it

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy dependencies and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app
COPY . .

# Expose port
EXPOSE 8000

# Corrected CMD for Flask with Gunicorn
CMD ["gunicorn", "server:app", "--bind", "0.0.0.0:8000"]

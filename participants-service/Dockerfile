# Use the official lightweight Python image
FROM python:3.11-slim

# Install SQLite
RUN apt-get update && apt-get install -y sqlite3

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install necessary dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port (if this service needs to be accessed directly)
EXPOSE 8080

# Run the application
CMD ["python", "app.py"]

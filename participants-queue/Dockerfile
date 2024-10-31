# Use Python base image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Add the wait-for-it.sh script to /app
COPY wait-for-it.sh /app/
RUN chmod +x /app/wait-for-it.sh

# Copy the consumer script and requirements.txt
COPY participants-queue.py /app/
COPY requirements.txt /app/

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Set the default command to run the consumer
CMD ["python", "participants-queue.py"]


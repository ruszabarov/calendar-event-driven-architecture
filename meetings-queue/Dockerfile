# Use Python base image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the consumer script and requirements.txt
COPY meetings-queue.py /app/
COPY requirements.txt /app/

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Set the default command to run the consumer
CMD ["python", "meetings-queue.py"]


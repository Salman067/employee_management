# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app/

# Install the required dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that Django will run on (default is 8000)
EXPOSE 8000

# Set environment variables for Django settings
ENV PYTHONUNBUFFERED 1



# Run the Django application
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

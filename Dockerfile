# Use the official Python image as a parent image
FROM python:3.8-slim

# Set environment variables for Python and Django
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE LunchApp.settings

# Create and set the working directory
RUN mkdir /app
WORKDIR /app

# Copy the requirements file into the container and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project code into the container
COPY . /app/

# Expose the port the application runs on
EXPOSE 8000

# Start the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

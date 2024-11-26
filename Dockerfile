# Use the official Python image as the base
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Expose port 8000 for the Django application
EXPOSE 8000

# Run the database population script and then start the server
CMD ["sh", "-c", "python scripts/populate_data.py && python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]

# Stage 1: Base Image
# We'll start with a lean, official Python 3.11 image.
FROM python:3.11-slim

# Stage 2: Set Working Directory
# Create a folder named /app inside the container to hold our project.
WORKDIR /app

# Stage 3: Install Dependencies
# Copy the requirements file first. This is an optimization trick.
# Docker caches this step, so it only re-installs dependencies if requirements.txt changes.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 4: Copy Application Code
# Copy all the other files from your project into the /app folder in the container.
COPY . .

# Stage 5: The Run Command
# This command will execute when the container starts.
# The --host 0.0.0.0 is crucial for making the server accessible from outside the container.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# Use the official Python base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables (optional but useful)
ENV REDIS_HOST=localhost
ENV REDIS_PORT=6379

# Expose the port Streamlit will run on
EXPOSE 8501

# Run Streamlit when the container starts
CMD ["streamlit", "run", "app.py"]

# Use the official Python base image
FROM python:3.11-slim

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Set the working directory in the container
WORKDIR /app

# Expose port 8080 for running the website
EXPOSE 8080

# Copy the required files
COPY app.py footer.py requirements.txt robots.txt sitemap.xml ./
COPY assets assets
COPY callbacks callbacks
COPY pages pages

# Create a virtual environment and activate it
RUN python -m venv venv
ENV PATH="/app/venv/bin:$PATH"

# Install dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Specify the command to run the app
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=8080"]

# Use the official Python image from the Docker Hub
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the entire application code into the container
COPY . /app

# Install the dependencies
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Install Google Chrome
RUN apt-get update && apt-get install -y wget unzip && \
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb && \
    apt-get clean 

# Expose the port that the Flask app runs on
EXPOSE 5000

# Command to run the Gunicorn server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]

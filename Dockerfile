# Define the ARG variable before the FROM statement
ARG PORT=443

# Use the cypress/browsers:latest image as the base image
FROM cypress/browsers:latest

# Install python3 and pip using apk
RUN apk update && apk add --no-cache python3 py3-pip

# Set the user base directory for pip
RUN echo $(python3 -m site --user-base)

# Copy requirements.txt to the working directory
COPY requirements.txt .

# Set the environment variable for the PATH
ENV PATH /root/.local/bin:$PATH

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Expose the specified port
EXPOSE $PORT

# Run the application using gunicorn
CMD ["gunicorn", "app:app"]

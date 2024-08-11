# Use Python image from the Docker Hub
FROM arm32v7/python:3
ENV SPI_PATH /app/SPI-Py
WORKDIR /app

# Install system dependencies
RUN apt-get update

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhost.org -r requirements.txt 

# Install the relevant modules
RUN pip3 install --no-cache-dir rpi.gpio

# Copy the rest of the application code into the container
COPY . .

WORKDIR $SPI_PATH
RUN python3 setup.py install

WORKDIR /app
# Run the Python script
CMD ["python", "-u", "main.py"]
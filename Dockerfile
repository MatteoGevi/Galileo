# Use an official PyTorch runtime as a parent image
FROM pytorch/pytorch:1.8.1-cuda10.2-cudnn7-runtime

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME galileo_env

# Run app.py when the container launches
CMD ["python", "app.py"]
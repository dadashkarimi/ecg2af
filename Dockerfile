# Use the base image from ML4H
FROM ghcr.io/broadinstitute/ml4h:tf2.9-latest-cpu

# Set the working directory inside the container
WORKDIR /app

# Copy the entire app directory into the container
COPY app/ ./app
COPY ml4h/ ./ml4h
COPY uploads/ ./uploads

# Copy the model_zoo directory, containing your ECG2AF model
COPY model_zoo/ ./model_zoo

# Copy the requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Create the uploads directory for storing uploaded files
RUN mkdir -p /app/uploads

# Expose the port that Flask will run on (default is 5000)
EXPOSE 5000

# Command to run the Flask app (assuming app.py is already inside the app directory)
CMD ["python", "app/app.py"]


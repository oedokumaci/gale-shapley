# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container
COPY . /usr/src/app

# Install PDM (Python Dependency Manager)
RUN pip install pdm

# Install dependencies and pre-commit hooks
RUN make setup

# Set environment variables
ENV number_of_simulations=1

# Run the command to start the app
CMD make run number_of_simulations=$number_of_simulations

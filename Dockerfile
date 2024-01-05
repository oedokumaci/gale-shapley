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

# Command to run tests
CMD ["pdm", "run", "test"]

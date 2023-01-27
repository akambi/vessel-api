# We will be using the official Python 3 Docker image.
FROM python:3.10-alpine as base
# Set the working directory to /usr/src/app.
WORKDIR /code

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

FROM base as dependencies
RUN pip install --upgrade pip
RUN pip install requests beautifulsoup4 python-dotenv

# Copy the file from the local host to the filesystem of the container at the working directory.
COPY requirements.txt ./

# Install all dependencies specified in requirements.txt.
RUN pip3 install --no-cache-dir -r requirements.txt

FROM dependencies as develop
# Copy the project source code from the local host to the filesystem of the container at the working directory.
COPY . .

CMD ["flask", "run"]

# Pull base image
FROM python:3.8

# Set work directory
WORKDIR /diaryspace

COPY . /diaryspace/

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# !!!: You will have to do the same below on your host
# !!!: if you're going to use docker-compose-dev.yml. 

# Install Python dependencies
RUN pip install pipenv && pipenv install --deploy --system

# Install Yarn
RUN apt update && apt install -y npm && npm install -g yarn
# Pull Yarn packages from yarn.lock
RUN yarn

# Copy static files from Yarn packages to `staticfiles` for Django
RUN python manage.py collectstatic

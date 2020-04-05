# Pull base image
FROM python:3.8

# Set work directory
WORKDIR /diaryspace

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# !!!: You will have to do the same below manually on your host
# !!!: if you intend to use docker-compose-dev.yml.

# Copy Python dependency descriptions
COPY Pipfile Pipfile.lock ./
# Install Python dependencies
RUN pip install pipenv && pipenv install --deploy --system

COPY package.json yarn.lock ./
# Install Yarn
RUN apt update && apt install -y npm && npm install -g yarn
# Pull Yarn packages from yarn.lock
RUN yarn

# Copy project files
COPY . .

# Copy static files from Yarn packages to `staticfiles` for Django
RUN python manage.py collectstatic

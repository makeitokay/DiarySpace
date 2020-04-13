# Pull base image
FROM python:3.8-alpine

# Set work directory
WORKDIR /diaryspace

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# !!!: You will have to do the same below manually on your host
# !!!: if you intend to use docker-compose-dev.yml.

# Install npm & Yarn
RUN apk add --no-cache npm && npm install -g yarn

# Install PostgreSQL libs
RUN apk add --no-cache gcc musl-dev postgresql-dev

# Copy Python dependency descriptions
COPY Pipfile Pipfile.lock ./
# Install Python dependencies
RUN pip install pipenv && pipenv install --deploy --system

COPY package.json yarn.lock ./
# Pull Yarn packages from yarn.lock
RUN yarn

# Copy project files
COPY . .

# Copy static files from Yarn packages to `staticfiles` for Django
RUN python manage.py collectstatic

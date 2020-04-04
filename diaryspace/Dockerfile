# Pull base image
FROM python:3.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /diaryspace

# Copy Python dependency description
COPY Pipfile Pipfile.lock /diaryspace/
# Install Python dependencies
RUN pip install pipenv && pipenv install --deploy --system

# Copy Yarn dependency description
COPY package.json yarn.lock /diaryspace/
# Install Yarn
RUN apt update && apt install -y npm && npm install -g yarn
# Pull Yarn packages from yarn.lock
RUN yarn

# Copy project
COPY . /diaryspace/

# Copy static files from Yarn packages to `staticfiles` for Django
RUN echo yes | python manage.py collectstatic

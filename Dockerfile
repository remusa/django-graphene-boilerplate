# Dockerfile

# Pull base image
FROM python:3.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# ENV DEBUG 0

# Set work directory
WORKDIR /code

# Install psycopg2
RUN apk update \
  && apk add --virtual build-deps gcc python3-dev musl-dev \
  && apk add postgresql-dev \
  && pip install psycopg2 \
  && apk del build-deps

# Install dependencies
RUN pip install pipenv
COPY Pipfile Pipfile.lock /code/
RUN pipenv install --system

# Alternative install
# COPY ./requirements.txt .
# RUN pip install -r requirements.txt

# Copy project
COPY . /code/

# # add and run as non-root user
# RUN adduser -D myuser
# USER myuser

# # run gunicorn
# CMD gunicorn hello_django.wsgi:application --bind 0.0.0.0:$PORT

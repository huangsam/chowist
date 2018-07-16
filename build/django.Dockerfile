FROM python:3.7-alpine
ENV PYTHONUNBUFFERED 1
WORKDIR /app
RUN apk add --no-cache --update \
    postgresql-dev \
    gcc \
    python3-dev \
    musl-dev
ADD Pipfile ./Pipfile
ADD Pipfile.lock ./Pipfile.lock
RUN pip install pipenv && pipenv install --system
ADD . ./
EXPOSE 8000
CMD sh entrypoints/django.sh

FROM python:3.8-alpine
ENV PYTHONUNBUFFERED 1
ENV PIP_NO_BINARY psycopg2
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

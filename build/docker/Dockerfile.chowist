FROM python:3.13-alpine

WORKDIR /app
COPY . ./

ENV PYTHONUNBUFFERED 1
ENV PIP_NO_BINARY psycopg2

RUN apk add --no-cache --update postgresql-dev python3-dev musl-dev gcc
RUN pip install -r requirements.txt

EXPOSE 8000

CMD sh entrypoints/django.sh

FROM python:3.13-alpine
ENV PYTHONUNBUFFERED 1
ENV PIP_NO_BINARY psycopg2
WORKDIR /app
RUN apk add --no-cache --update \
    postgresql-dev \
    gcc \
    python3-dev \
    musl-dev
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY . ./
EXPOSE 8000
CMD sh entrypoints/django.sh

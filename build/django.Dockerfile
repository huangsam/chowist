FROM python:3.6-alpine
ENV PYTHONUNBUFFERED 1
WORKDIR /app
RUN apk add --no-cache --update \
    postgresql-dev \
    gcc \
    python3-dev \
    musl-dev
ADD requirements requirements
RUN pip install -r requirements/all.txt
ADD . ./
EXPOSE 8000
CMD sh entrypoint.sh

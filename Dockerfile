FROM python:3.6.2

ADD requirements.txt /src/requirements.txt
RUN pip install -r /src/requirements.txt
WORKDIR /src

CMD ["gunicorn", "chowist.wsgi", "-b", "0.0.0.0:8000", "-w", "4"]
EXPOSE 8000

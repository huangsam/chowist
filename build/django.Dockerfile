FROM python:3.6-alpine
WORKDIR /app
ADD requirements requirements
RUN pip install -r requirements/all.txt
ADD . ./
EXPOSE 8000
CMD sh entrypoint.sh

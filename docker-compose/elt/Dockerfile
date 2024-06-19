FROM python:latest
# FROM python:3.8-slim

RUN apt-get update && apt-get install -y postgresql-client

COPY run.sh /app/run.sh

WORKDIR /usr/src/app

COPY elt.py /usr/src/app/

CMD ["python3", "elt.py"]
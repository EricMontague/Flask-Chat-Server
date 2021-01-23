FROM python:3.7.7-alpine3.11

RUN adduser -D chat_app

WORKDIR /home/chat_app

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt


COPY app app
COPY aws_services_setup aws_services_setup
COPY tests tests
COPY .env .env
COPY chat_app.py cli.py config.py conftest.py logging.conf ./


EXPOSE 5000
CMD python chat_app.py

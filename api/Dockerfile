FROM python:3.7.7-alpine3.11
WORKDIR /home/chat_app


COPY requirements.txt requirements.txt
COPY app app
COPY aws_services_setup aws_services_setup
COPY tests tests
COPY .env .env
COPY chat_app.py cli.py config.py conftest.py logging.conf ./


RUN apk update \
  && apk add --virtual build-dependencies libffi-dev openssl-dev python3-dev musl-dev py-pip build-base \
  && apk add jpeg-dev zlib-dev libjpeg \
  && pip install --upgrade pip \
  && pip install -r requirements.txt \
  && apk del build-dependencies 
  

EXPOSE 5000
CMD ["sh", "-c", "python cli.py create-table && python cli.py fake-data $LOAD && python chat_app.py"]


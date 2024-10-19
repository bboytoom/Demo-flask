FROM python:3.12

RUN apt update -y && \
    apt upgrade -y && \
    apt-get install -y python3-pip default-mysql-client

ENV APP_DIR /app

RUN mkdir $APP_DIR
WORKDIR $APP_DIR

COPY requirements.txt $APP_DIR

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "wsgi.py"]

FROM python:3.10-slim

ARG APP_DIR=/var/www/app

WORKDIR ${APP_DIR}

RUN apt-get update \
    && apt-get install -y postgresql \
    && apt-get install -y gcc \
    && apt-get install -y python3-dev \
    && apt-get install -y musl-dev

COPY . ${APP_DIR}

RUN pip install -r requirements.txt

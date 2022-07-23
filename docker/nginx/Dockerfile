FROM nginx:alpine

RUN apk update && apk upgrade && apk add --no-cache bash

RUN set -x ; \
    addgroup -g 82 -S www-data ; \
    adduser -u 82 -D -S -G www-data www-data && exit 0 ; exit 1

ARG APPLICATION_ADDRESS=localhost
# It must be a name of container which contains application
ARG UPSTREAM_CONTAINER=django_app
ARG APP_DIR=/var/www/app/
ARG APP_FOLDER=app
RUN echo \
"upstream app { server ${UPSTREAM_CONTAINER}:8000; }"\
"server {"\
    "server_name ${APPLICATION_ADDRESS};"\
    "listen 80;"\
    "location / {"\
        "proxy_pass http://app;"\
        "proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;"\
        "proxy_set_header Host \$host;"\
        "proxy_redirect off;"\
    "}"\
    "location /static/ {"\
        "alias ${APP_DIR}/${APP_FOLDER}/static/;"\
    "}"\
    "location /media/ {"\
        "alias ${APP_DIR}/${APP_FOLDER}/media/;"\
    "}"\
"}" > /etc/nginx/conf.d/app.conf

EXPOSE 80

FROM nginx:alpine

RUN apk update && apk upgrade && apk add --no-cache bash

RUN set -x ; \
    addgroup -g 82 -S www-data ; \
    adduser -u 82 -D -S -G www-data www-data && exit 0 ; exit 1

ARG UPSTREAM_NAME=app
# It must be a name of container which contains application
ARG UPSTREAM_CONTAINER=django_app
ARG UPSTREAM_PORT=8000
RUN echo \
"upstream ${UPSTREAM_NAME} { server ${UPSTREAM_CONTAINER}:${UPSTREAM_PORT}; }\n\
server {\n\
    listen 80;\n\
    location / {\n\
        proxy_pass http://${UPSTREAM_NAME};\n\
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;\n\
        proxy_set_header Host \$host;\n\
        proxy_redirect off;\n\
    }\n\
    location /static/ {\n\
        alias /code/static/;\n\
    }\n\
    location /media/ {\n\
        alias /code/media/;\n\
    }\n\
}" > /etc/nginx/conf.d/app.conf


EXPOSE 80

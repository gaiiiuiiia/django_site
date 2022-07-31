#!/bin/bash

echo "upstream app { server $UPSTREAM_CONTAINER:8000; }"\
"server {"\
    "server_name $APPLICATION_ADDRESS;"\
    "listen 80;"\
    "location / {"\
        "proxy_pass http://app;"\
        "proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;"\
        "proxy_set_header Host \$host;"\
        "proxy_redirect off;"\
    "}"\
    "location /static/ {"\
        "alias $APP_DIR/$APP_FOLDER/static/;"\
    "}"\
    "location /media/ {"\
        "alias $APP_DIR/$APP_FOLDER/media/;"\
    "}"\
"}" > /etc/nginx/conf.d/app.conf

exec "$@"

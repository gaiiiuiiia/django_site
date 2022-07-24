#!/bin/sh

IS_NEW_PROJECT=0
if ! [ -d "$APP_DIR/$APP_FOLDER" ]; then
  echo "'$APP_FOLDER' does not exist. A new project will be create in the '$APP_FOLDER' directory"
  django-admin startproject $APP_FOLDER
  IS_NEW_PROJECT=1
else
  echo "'$APP_FOLDER' is exists. Continuing"
fi

cd $APP_DIR/$APP_FOLDER

if ! [ -f "manage.py" ]; then
  echo "Incorrect directory! The file 'manage.py' is not here!"
  echo "Please check the '$APP_DIR/$APP_FOLDER' directory."
  echo "EXIT :("
  exit 1
fi

sleep 10

if [ $IS_NEW_PROJECT -eq 0 ]; then \
  python manage.py migrate
  python manage.py createcachetable
  python manage.py collectstatic --noinput
fi

gunicorn $APP_FOLDER.wsgi --bind 0.0.0.0:8000

exec "$@"

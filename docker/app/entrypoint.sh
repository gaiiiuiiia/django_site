#!/bin/sh

# ====== CREATE NEW PROJECT IF IT NOT EXIST ======
IS_NEW_PROJECT=0
APP_FOLDER_PATH=$APP_DIR/$APP_FOLDER
if ! [ -d "$APP_FOLDER_PATH" ]; then
  echo "'$APP_FOLDER_PATH' does not exist. A new django project will be create in the '$APP_FOLDER_PATH' directory"
  django-admin startproject $APP_FOLDER
  IS_NEW_PROJECT=1
else
  echo "'$APP_FOLDER_PATH' is exists. Continuing"
fi

# ====== CHECK IF manage.py file in application directory ======
if ! [ -f "$APP_FOLDER_PATH/manage.py" ]; then
  echo "Incorrect directory! The file 'manage.py' is not here!"
  echo "Please check the '$APP_FOLDER_PATH' directory."
  echo "EXIT :("
  exit 1
fi

# ====== CREATE A STATIC DIRECTORY IF IT NOT EXIST ======
STATIC_FOLDER_PATH=$APP_DIR/$APP_FOLDER/$STATIC_FILES_FOLDER
if ! [ -d "$STATIC_FOLDER_PATH" ]; then
  echo "create static at $STATIC_FOLDER_PATH"
  mkdir $STATIC_FOLDER_PATH
fi

# ====== CREATE A MEDIA DIRECTORY IF IT NOT EXIST ======
MEDIA_FOLDER_PATH=$APP_DIR/$APP_FOLDER/$MEDIA_FILES_FOLDER
if ! [ -d "$MEDIA_FOLDER_PATH" ]; then
  echo "create media at $MEDIA_FOLDER_PATH"
  mkdir $MEDIA_FOLDER_PATH
fi

cd $APP_DIR/$APP_FOLDER

sleep 10

if [ $IS_NEW_PROJECT -eq 0 ]; then \
  python manage.py migrate
  python manage.py createcachetable
  python manage.py collectstatic --noinput
fi

gunicorn $APP_FOLDER.wsgi --bind 0.0.0.0:8000

exec "$@"

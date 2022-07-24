Как разворачивать

См. файл .env.dist. Основные конфигурации приложения находятся в нем.
Разрабатывал деплой по статье https://matakov.com/django-postgres-nginx-s-pomoshhyu-docker-compose/

При запуске docker-compose up будут подняты три контейнера. Приложение, Сервер и БД.

добавить в /etc/hosts новый адрес 127.0.0.1   ${APPLICATION_ADDRESS}

выполнить docker-compose build из папки docker

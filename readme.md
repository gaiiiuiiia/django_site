Как разворачивать

См. файл .env.dist. Основные конфигурации приложения находятся в нем.
Разрабатывал деплой по статье https://matakov.com/django-postgres-nginx-s-pomoshhyu-docker-compose/

При запуске docker-compose up будут подняты три контейнера. Приложение, Сервер и БД.

добавить в /etc/hosts новый адрес 127.0.0.1   ${APPLICATION_ADDRESS}

Предположим, что директории app не существует. 
Перед поднятием контейнеров docker-compose up -- build, необходимо закомментировать 
вольюмы к static и media у сервисов app и webserver.
После первого поднятия контейнеров, создастся директория с чистым проектом на Django.
Необходимо в файле settings.py указать допустимый хост - см. ${APPLICATION_ADDRESS}, путь к static файлам:
STATIC_ROOT = os.path.join(BASE_DIR, 'static').
После этого надо остановить контейнеры docker-compose down, раскомментировать вольюмы и поднять их еще раз. После второго 
поднятия контейнеров будут выполнен сбор статических файлов и миграции.


При желании использовать flake8 - код линтера, можно поставить локально виртуальное окружение и 
выполнить pip install -r requirements_local.txt --no-cache.
Советы по настройке flake8 см. на https://melevir.medium.com/pycharm-loves-flake-671c7fac4f52

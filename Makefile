##################
# Docker compose
##################

dc_build:
	docker-compose -f ./docker/docker-compose.yaml build

dc_start:
	docker-compose -f ./docker/docker-compose.yaml start

dc_stop:
	docker-compose -f ./docker/docker-compose.yaml stop

dc_up:
	docker-compose -f ./docker/docker-compose.yaml up -d --remove-orphans

dc_ps:
	docker-compose -f ./docker/docker-compose.yaml ps

dc_logs:
	docker-compose -f ./docker/docker-compose.yaml logs -f

dc_down:
	docker-compose -f ./docker/docker-compose.yaml down -v --remove-orphans


##################
# App
##################

app_bash:
	docker-compose -f ./docker/docker-compose.yaml exec app /bin/bash
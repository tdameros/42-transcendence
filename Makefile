DOCKER_COMPOSE_PATH		=	docker-compose.yaml
DOCKER_COMPOSE			=	docker compose -f $(DOCKER_COMPOSE_PATH)
DOCKER_COMPOSE_TIMEOUT	=	--timeout 1

FRONT_DB_VOLUME_PATH			=	front/docker/volumes/db
USER_MANAGEMENT_DB_VOLUME_PATH	=	user_management/docker/volumes/db
USER_STATS_DB_VOLUME_PATH		=	user_stats/docker/volumes/db
MATCHMAKING_DB_VOLUME_PATH		=	matchmaking/docker/volumes/db
TOURNAMENT_DB_VOLUME_PATH		=	tournament/docker/volumes/db
NOTIFICATION_DB_VOLUME_PATH		=	notification/docker/volumes/db

FRONT_DIST_VOLUME_PATH          =   front/app/dist

DB_VOLUMES						=	$(FRONT_DB_VOLUME_PATH) \
									$(USER_MANAGEMENT_DB_VOLUME_PATH) \
									$(USER_STATS_DB_VOLUME_PATH) \
									$(MATCHMAKING_DB_VOLUME_PATH) \
									$(TOURNAMENT_DB_VOLUME_PATH) \
									$(NOTIFICATION_DB_VOLUME_PATH)

VOLUMES                         =   $(FRONT_DIST_VOLUME_PATH) \
                                    $(DB_VOLUMES)

.PHONY: all
all:
	$(MAKE) up

.PHONY: up
up: create_volume_path
	$(DOCKER_COMPOSE) up --detach --build

.PHONY: down
down:
	$(DOCKER_COMPOSE) down $(DOCKER_COMPOSE_TIMEOUT)

.PHONY: start
start:
	$(DOCKER_COMPOSE) start

.PHONY: stop
stop:
	$(DOCKER_COMPOSE) stop $(DOCKER_COMPOSE_TIMEOUT)

.PHONY: restart
restart:
	$(DOCKER_COMPOSE) restart $(DOCKER_COMPOSE_TIMEOUT)

.PHONY: clean
clean:
	$(DOCKER_COMPOSE) down $(DOCKER_COMPOSE_TIMEOUT) --volumes --rmi all

.PHONY: fclean
fclean: clean
	$(MAKE) delete_volume_path

.PHONY: re
re: fclean
	$(MAKE) all

.PHONY: create_volume_path
create_volume_path:
	mkdir -p $(VOLUMES)

.PHONY: delete_volume_path
delete_volume_path:
	$(RM) -r $(VOLUMES)

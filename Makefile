DOCKER_COMPOSE_PATH		=	docker-compose.yaml
DOCKER_COMPOSE			=	docker compose -f $(DOCKER_COMPOSE_PATH)
DOCKER_COMPOSE_TIMEOUT	=	--timeout 1

USER_MANAGEMENT_DB_VOLUME_PATH	=	user_management/docker/volumes/db
USER_STATS_DB_VOLUME_PATH		=	user_stats/docker/volumes/db
MATCHMAKING_DB_VOLUME_PATH		=	matchmaking/docker/volumes/db
TOURNAMENT_DB_VOLUME_PATH		=	tournament/docker/volumes/db
NOTIFICATION_DB_VOLUME_PATH		=	notification/docker/volumes/db


FRONT_DIST_VOLUME_PATH          =   front/docker/volumes/dist
USER_MANAGEMENT_MEDIA_VOLUME_PATH=	user_management/docker/volumes/media

DB_VOLUMES						=	$(USER_MANAGEMENT_DB_VOLUME_PATH) \
									$(USER_STATS_DB_VOLUME_PATH) \
									$(MATCHMAKING_DB_VOLUME_PATH) \
									$(TOURNAMENT_DB_VOLUME_PATH) \
									$(NOTIFICATION_DB_VOLUME_PATH)

VOLUMES                         =   $(FRONT_DIST_VOLUME_PATH) \
									$(USER_MANAGEMENT_MEDIA_VOLUME_PATH) \
                                    $(DB_VOLUMES)

SSL_IMAGE_NAME                  =   ssl_certificate_generator

.PHONY: all
all:
	if [ ! -e ssl/certs/certificate.crt ] && [ ! -e ssl/certs/certificate.crt ]; then \
  		$(MAKE) generate_ssl_certificate; \
  		echo "SSL certificate generated"; \
    fi
	$(MAKE) up

.PHONY: generate_ssl_certificate
generate_ssl_certificate:
	docker build -t $(SSL_IMAGE_NAME) ./ssl
	mkdir -p ssl/certs
	docker run -v ./ssl/certs:/app/ssl $(SSL_IMAGE_NAME)
	$(MAKE) delete_ssl_container

.PHONY: generate_env
generate_env:
	python3 ./common/src/generate_env.py

.PHONY: up
up: create_volume_path
	$(DOCKER_COMPOSE) up --detach --build

.PHONY: down
down:
	$(DOCKER_COMPOSE) down $(DOCKER_COMPOSE_TIMEOUT)

.PHONY: reup
reup: down
	$(MAKE) up

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
clean: delete_ssl_image
	$(DOCKER_COMPOSE) down $(DOCKER_COMPOSE_TIMEOUT) --volumes --rmi all

.PHONY: fclean
fclean: clean
	$(MAKE) delete_volume_path
	rm -rf ./ssl/certs

.PHONY: re
re: fclean
	$(MAKE) all

.PHONY: create_volume_path
create_volume_path:
	mkdir -p $(VOLUMES)

.PHONY: delete_volume_path
delete_volume_path:
	$(RM) -r $(VOLUMES)

.PHONY: delete_ssl_container
delete_ssl_container:
	docker rm -f $$(docker ps -a -q -f ancestor=$(SSL_IMAGE_NAME))

.PHONY: delete_ssl_image
delete_ssl_image:
	if docker images | grep -q "$(SSL_IMAGE_NAME)"; then \
		docker rmi $(SSL_IMAGE_NAME); \
    fi

.PHONY: delete_env
delete_env:
	find . -name ".env" -delete

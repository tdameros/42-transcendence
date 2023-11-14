DOCKER_COMPOSE_PATH = docker-compose.yaml

.PHONY: all
all:
	@mkdir -p src/front/docker/volumes/db/
	@mkdir -p src/user_management/docker/volumes/db/
	@mkdir -p src/matchmaking/docker/volumes/db/
	docker-compose -f $(DOCKER_COMPOSE_PATH) up -d --build #&& docker logs -f transcendence

.PHONY: stop
stop:
	docker-compose -f $(DOCKER_COMPOSE_PATH) kill

.PHONY: clean
clean: stop
	docker-compose -f $(DOCKER_COMPOSE_PATH) down -v

.PHONY: fclean
fclean: clean

.PHONY: re
re: fclean
	$(MAKE) all

# Docker Compose
COMPOSE = docker compose --env-file .env -f docker/compose.yaml

.PHONY: up down restart logs ps build pull clean format lint typecheck test

# ==========================
# Docker Commands
# ==========================

up:
	$(COMPOSE) up -d

down:
	$(COMPOSE) down

restart:
	$(COMPOSE) down
	$(COMPOSE) up -d

logs:
	$(COMPOSE) logs -f

ps:
	$(COMPOSE) ps

build:
	$(COMPOSE) build

pull:
	$(COMPOSE) pull

clean:
	$(COMPOSE) down -v --remove-orphans

# ==========================
# Code Quality
# ==========================

format:
	black src tests
	isort src tests

lint:
	ruff check src tests

typecheck:
	mypy src

test:
	pytest -v
# Docker Compose
COMPOSE=docker compose --env-file .env -f docker/compose.yaml

.PHONY: up down restart logs ps

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

# Code Quality
.PHONY: format lint typecheck test

format:
	black src tests
	isort src tests

lint:
	ruff check src tests

typecheck:
	mypy src

test:
	pytest -v
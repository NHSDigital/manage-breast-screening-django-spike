include scripts/shared.mk
include scripts/terraform/terraform.mk

clean:: _clean-docker  # Clean-up project resources (main) @Operations

# Configure development environment (main) @Configuration
config: manage_breast_screening/config/.env \
	_install-tools \
	_install-poetry \
	githooks-config \
	dependencies \
	assets \
	db migrate seed

dependencies: # Install dependencies needed to build and test the project @Pipeline
	poetry install
	npm install

assets: # Compile assets @Pipeline
	npm run compile
	poetry run playwright install

build: # Build the project artefact @Pipeline
	docker build -t "app:$$(git rev-parse HEAD)" .

deploy: # Deploy the project artefact to the target environment @Pipeline
	# TODO: Implement the artefact deployment step

githooks-config:
	if ! command -v pre-commit >/dev/null 2>&1; then \
		pip install pre-commit; \
	fi
	pre-commit install

githooks-run: # Run git hooks configured in this repository @Operations
	pre-commit run \
		--config scripts/config/pre-commit.yaml \
		--all-files

help: # Print help @Others
	printf "\nUsage: \033[3m\033[93m[arg1=val1] [arg2=val2] \033[0m\033[0m\033[32mmake\033[0m\033[34m <command>\033[0m\n\n"
	perl -e '$(HELP_SCRIPT)' $(MAKEFILE_LIST)

test: test-unit test-ui test-lint # Run all tests @Testing

test-unit: # Run unit tests @Testing
	poetry run pytest -m 'not system'
	npm test -- --coverage

test-lint: # Lint files @Testing
	npm run lint
	poetry run ruff check manage_breast_screening

test-ui: # Run UI tests @Testing
	poetry run pytest -m system

run: manage_breast_screening/config/.env # Start the development server @Development
	poetry run ./manage.py runserver

db: manage_breast_screening/config/.env # Start the development database @Development
	docker compose --env-file manage_breast_screening/config/.env up -d --wait

local: db run

rebuild-db: _clean-docker db migrate seed  # Create a fresh development database @Development

migrate:  # Run migrations
	poetry run ./manage.py migrate

seed:  # Load seed data
	poetry run ./manage.py loaddata clinics participants

models:
	poetry run ./manage.py shell -c "from django.apps import apps; print('\n'.join(f'{m._meta.app_label}.{m.__name__}' for m in apps.get_models()))"

shell:
	poetry run ./manage.py shell

erd:
	poetry run python -m django_diagram --settings manage_breast_screening.config.settings --output docs/diagrams/erd.md
	sed -i '' '1s/^/```mermaid\n/' docs/diagrams/erd.md && printf '\n```\n' >> docs/diagrams/erd.md

_install-poetry:
	if ! command -v poetry >/dev/null 2>&1; then \
		pip install poetry; \
	else \
		echo "poetry already installed"; \
	fi

_clean-docker:
	docker compose --env-file manage_breast_screening/config/.env down -v # remove the volume if it exists

manage_breast_screening/config/.env:
	cp manage_breast_screening/config/.env.tpl manage_breast_screening/config/.env


.DEFAULT_GOAL := help
.PHONY: clean config dependencies build deploy githooks-config githooks-run help test test-unit test-lint test-ui run _install-poetry _clean-docker rebuild-db db migrate seed shell
.SILENT: help run

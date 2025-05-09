

include scripts/shared.mk

clean:: # Clean-up project resources (main) @Operations

config: manage_breast_screening/config/.env _install-dependencies githooks-config _install_poetry _first_time_django_setup  # Configure development environment (main) @Configuration

dependencies: # Install dependencies needed to build and test the project @Pipeline
	poetry install
	npm install
	npm run compile

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

test: test-unit test-lint # Run all tests @Testing

test-unit: # Run unit tests @Testing
	poetry run pytest

test-lint: # Lint files @Testing
	# TODO

test-ui: # Run UI tests @Testing
	# TODO

run: manage_breast_screening/config/.env # Run the development server @Development
	poetry run ./manage.py runserver

_install_poetry:
	if ! command -v poetry >/dev/null 2>&1; then \
		pip install poetry; \
	else \
		echo "poetry already installed"; \
	fi

_first_time_django_setup:
	poetry install
	poetry run ./manage.py migrate
	poetry run ./manage.py loaddata clinics participants
	npm install
	npm run compile:css

manage_breast_screening/config/.env:
	cp manage_breast_screening/config/.env.tpl manage_breast_screening/config/.env


.DEFAULT_GOAL := help
.PHONY: clean config dependencies build deploy githooks-config githooks-run help test test-unit test-lint test-ui run _install_poetry _first_time_django_setup
.SILENT: help run

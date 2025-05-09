# Manage breast screening Django spike

[![Main branch CI](https://github.com/nhsdigital/manage-breast-screening-django-spike/actions/workflows/cicd-2-main-branch.yaml/badge.svg)](https://github.com/nhsdigital/manage-breast-screening-django-spike/actions/workflows/cicd-2-main-branch.yaml)

This repo is a spike to explore using Django as the framework for our new service.

The new service is a system for managing breast screening clinics, including:

- Viewing and managing daily clinic lists
- Tracking participants through their screening journey
- Managing participant information and status

## Running the app

## Setup

To install the toolchain dependencies and setup the project, run

```shell
make config
```

This command assumes you have a few things already installed:

- [Docker](https://www.docker.com/) container runtime or a compatible tool, e.g. [Podman](https://podman.io/)
- [asdf](https://asdf-vm.com/) version manager
- [GNU make](https://www.gnu.org/software/make/) 3.82 or later

## Usage

```sh
make run
```

This will serve the app at http://localhost:8000

## Local development

### Tests

To run all the tests:

```sh
make test
```

### Dependency management
Python dependencies are managed via [poetry](https://python-poetry.org/docs/basic-usage/).

- `poetry install` installs dependencies from the lockfile
- `poetry add` and `poetry remove` adds and removes dependencies
- `poetry run [COMMAND]` runs a command in the context of the project's virtual environment

`npm` is used to manage javascript dependencies and frontend assets.

You can run `make dependencies` to install anything that's missing after pulling new changes from GitHub.

### Frontend assets

To compile assets, run `npm run compile`

To watch for changes, run `npm run watch`

This will compile scss files to css and bundle javascripts with [rollup.js](https://rollupjs.org/).

### Django admin
We'll probably remove it before deploying to production, but currently Django admin is enabled.

To use it, first create a superuser

```sh
poetry run ./manage.py createsuperuser
```

Then run the app and navigate to `http://localhost:8000/admin`

## Design

### Structure

The `manage_breast_screening` directory contains all the Django project code.

`config` is a subpackage containing the configuration. The other subpackages - such as `clinics` - are [Django apps](https://docs.djangoproject.com/en/5.1/ref/applications/). These each represent a bounded context within our overall domain of screening events. Django apps can be built with customisability and extendability in mind, and published as python packages, but we aren't doing that yet.

To generate a new app, run:

```sh
poetry run ./manage.py startapp <app_name> manage_breast_screening/`
```

## Contributing

- Make sure you have `pre-commit` running so that pre-commit hooks run automatically when you commit - this should have been set up automatically when you ran `make config`.
- Consider switching on format-on-save in your editor (e.g. [Black](https://github.com/psf/black) for python)
- (Internal contributions only) contact the `#screening-manage` team on slack with any questions

### Makefile and Scripts
`scripts/` contains various scripts that can be used in the CI/CD workflows.

For more information, see the following developer guides:

- [Bash and Make](https://github.com/NHSDigital/repository-template/blob/main/docs/developer-guides/Bash_and_Make.md)
- [Scripting Docker](https://github.com/NHSDigital/repository-template/blob/main/docs/developer-guides/Scripting_Docker.md)

## Licence
Unless stated otherwise, the codebase is released under the MIT License. This covers both the codebase and any sample code in the documentation. See [LICENCE.md](./LICENCE.md).

Any HTML or Markdown documentation is [© Crown Copyright](https://www.nationalarchives.gov.uk/information-management/re-using-public-sector-information/uk-government-licensing-framework/crown-copyright/) and available under the terms of the [Open Government Licence v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/).

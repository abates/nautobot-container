
# Nautobot

# How to use this repo

This repo is designed to provide a custom build of Nautobot to include a set of plugins which can then be used in a development environment or deployed in production.  Included in this repo is a skeleton Nautobot plugin which is designed only to provide a quick example of how a plugin could be developed.  Plugins should ultimately be built as packages, published to a pypi style repository and added to the poetry `pyproject.toml` in this repo.  The plugin code should be hosted in their own repositories with their own CI pipelines and not included here.

## Install Docker

Before beginning, install Docker and verify its operation by running `docker run hello-world`. If you encounter any issues connecting to the Docker service, check that your local user account is permitted to run Docker. **Note:** `docker-compose` v1.20.0 or later is required.

## Build and start Nautobot

You can build, deploy and populate Nautobot with the following steps
1. `invoke build`
2. `invoke start` or `invoke debug`

Nautobot will be available on port 80 locally http://localhost

## Cleanup Everything and start from scratch
1. `invoke destroy`
2. `invoke build`
3. `invoke db-import`
4. `invoke start`

## Export current database
While the database is already running
* `invoke db-export`

### Docker Compose Files

Several docker compose files are provided as [overrides](https://docs.docker.com/compose/extends/) to allow for various development configurations, these can be thought of as layers to docker compose, each compose file is described below:

- `docker-compose.requirements.yml` - Starts the required prerequisite redis and postgres services
- `docker-compose.base.yml` - Defines the Nautobot and the Nautobot worker service, how they should be run and built
- `docker-compose.dev.yml` - Defines the default dev environment running a single nautobot and worker containers, these containers have volumes and ports exposed to the local machine to allow for automatic reloading of any changes to python files as well as all development dependencies
- `docker-compose.local.yml` - Exposes the redis and postgres services to the local machine, this will allow users to run `nautobot-server` commands in their local poetry environments
- `docker-compose.dev-prod.yml` - Replaces the dev containers with prod containers, the main differences are the dev dependencies are not installed and there are no volumes, so any updates to the repo will require the containers to be rebuilt.  This is useful to test the final container builds locally.
- `docker-compose.prod.yml` - Provides an example compose file of what a production deployment of Nautobot in docker-compose might look like, adds multiple replicas, prometheus, and an nginx gateway.

## Local Poetry Development Environment

The development environment can be used in 2 ways, first with inside a docker container as detailed above, second is in a local poetry environment for advanced development.

### Local Poetry Development Environment

1.  Copy `environments/.creds.example.env` to `environments/creds.env` (This file will be ignored by git and docker)
2.  Define `NAUTOBOT_SECRET_KEY` in `environments/creds.env` if you are going to import the production DB you need to use the same secret key.
3.  Uncomment the `NAUTOBOT_DB_HOST`, `NAUTOBOT_REDIS_HOST`, and `NAUTOBOT_CONFIG` variables in `environments/creds.env`
4.  Create an invoke.yml with the following contents at the root of the repo:

```shell
---
nautobot_andrew_bates:
  local: True
  compose_files:
    - "docker-compose.requirements.yml"
    - "docker-compose.local.yml"
```

5.  Run the following commands:

```shell
poetry shell
poetry install
export $(cat environments/local_dev.env | xargs)
export $(cat environments/creds.env | xargs) 
```

6.  You can now run nautobot-server commands as you would from the [Nautobot documentation](https://nautobot.readthedocs.io/en/latest/) for example to start the development server:

```shell
nautobot-server runserver 0.0.0.0:8080 --insecure
```
# SSL

This repo contains a self-signed SSL certificate in `environments/nautobot.crt` and the private key in `environments/nautobot.key` these files are injected into the nginx and Nautobot containers to ensure traffic is encrypted to the nginx container and between the nginx and Nautobot containers.  These files can be replaced with signed certificates.  The system is designed to listen on both port 443 (https) and 80 (http), the recommendation is to use port 80 for only non-sensitive traffic such as health checks only.
# CLI Helper Commands

The project is coming with a CLI helper based on [invoke](http://www.pyinvoke.org/) to help manage the environments. The commands are listed below in 3 categories ` environment`, `utility` and `testing`. 

Each command can be executed with `invoke <command>`. All commands support the arguments `--environment`  if you want to manually define the environment to use. Each command also has its own help `invoke <command> --help`

## Manage environments
```
  build            Build all docker images.
  debug            Start Nautobot and its dependencies in debug mode.
  destroy          Destroy all containers and volumes.
  start            Start Nautobot and its dependencies in detached mode.
  stop             Stop Nautobot and its dependencies.
  db-export        Export Database data to nautobot_backup.dump.
  db-import        Import test data.
```

## Utility 
```
  cli              Launch a bash shell inside the running Nautobot container.
  makemigrations   Run Make Migration in Django.
  migrate          Run database migrations in Django.
  nbshell          Launch a nbshell session.
```
#### Testing 

```
  tests            Run all tests for this plugin.
  pylint           Run pylint code analysis.
  pydocstyle       Run pydocstyle to validate docstring formatting adheres to NTC defined standards.
  bandit           Run bandit to validate basic static code security analysis.
  black            Run black to check that Python files adhere to its style standards.
  unittest         Run Django unit tests for the plugin.
  yamllint         Run yamllint to validate Yaml files formatting.
```

# Nautobot Container

This project builds a Nautobot container that runs the Nautobot server
as well as the associated workers.

### Setup

Run setup_env.py to create the environment file necessary for Nautobot

The included docker-compose.yml file will start a postgresql database
container, a redis container and the nautobot server container. If not
using this file then the .env may need to be updated to reflect your
database and redis information.

# Nautobot Container

This project builds a Nautobot container that runs the Nautobot server
as well as the associated workers.

### Setup

Run `setup_env.py` to create the environment file necessary for Nautobot

The included `docker-compose.yml` file will start a postgresql database
container, a redis container and the nautobot server container. If not
using this file then the .env may need to be updated to reflect your
database and redis information.

### Plugin Installation

To add plugins to the container, simply add them to the plugin_requirements.txt
file. This file should be mapped as a bind mount in your docker-compose file,
mounted to /opt/nautobot/plugin_requirements.txt.  When the container boots
it will detect the file and automatically `run pip install -r`

### Plugin Configuration

Configuring plugins is similar to installing them.  Map the file
`plugin_config.py`, as a bind mount, to `/opt/nautobot/plugin_config.py`.
Add plugins and their configs in this file as outlined in the Nautobot
documentation.

For example the plugin_config.py could look like this:
```python
PLUGINS = [
    'plugin_name',
]

PLUGINS_CONFIG = {
    'plugin_name': {
        'foo': 'bar',
        'buzz': 'bazz'
    }
}
```

The config loading code only loads PLUGINS and PLUGINS_CONFIG, no other configuration
settings will be updated from plugin_config.py

# Developing Nautobot plugins 

One of the intended purposes of this repository is to make it simpler to develop Nautobot plugins.
This document lays out some tips and tricks for doing so.

## Creating a new plugin

We generally recommend that a plugin be implemented as a Python package named `nautobot_<pluginname>`, and for
convenience and consistency within this repository, that package should be isolated within the `plugins/<pluginname>`
directory. So to begin development on a new plugin, assuming you have [Poetry](https://python-poetry.org/) installed,
you would invoke:

```shell
mkdir plugins/pluginname
cd plugins/pluginname
poetry init --name nautobot_pluginname

git add ./pyproject.toml
mkdir ./nautobot_pluginname
```

Next you'll want to create an `__init__.py` inside your `nautobot_pluginname` directory, and in that file,
[define a `PluginConfig` subclass](https://nautobot.readthedocs.io/en/stable/plugins/development/#define-a-pluginconfig).

Once you have created this file, and added it to Git, you can add the newly created plugin to Nautobot
installation and configuration, as follows.

### Add the plugin installation to the Docker build

`environments/Dockerfile`:

```docker
WORKDIR /source/plugins/pluginname
RUN poetry install --no-interaction --no-ansi
```

### Ensure the plugin source is mounted dynamically into the development container

`environments/docker-compose.development.yml`:

```yaml
x-nautobot-base: &nautobot-base
  # ...
  volumes:
    # ...
    - ../plugins/pluginname/nautobot_pluginname:/source/plugins/pluginname/nautobot_pluginname
  # ...
```

### Add the plugin and plugin config to Nautobot

TODO

### Rebuild the development container and relaunch it

```shell
invoke stop build start
```

If all is well, you should shortly be able to log in to `http://localhost` and then navigate to
`http://localhost/admin/plugins/installed-plugins/` and see that your new plugin is shown as installed.


## Developing a plugin

You should be familiar with the relevant sections of the official Nautobot plugin development documentation,
which provides a good overview of developing a plugin that has its own:

- [database models](https://nautobot.readthedocs.io/en/stable/plugins/development/#database-models)
- [views](https://nautobot.readthedocs.io/en/stable/plugins/development/#views)
- [REST API endpoints](https://nautobot.readthedocs.io/en/stable/plugins/development/#rest-api-endpoints)
- [menu items](https://nautobot.readthedocs.io/en/stable/plugins/development/#navigation-menu-items)
- [extensions of existing views](https://nautobot.readthedocs.io/en/stable/plugins/development/#extending-core-templates)

### Developing models

During initial development of your plugin, you may end up making changes to the plugin's model definition
multiple times. To avoid creating multiple `migrations` files, you can use the following workflow to regenerate the
`0001_initial.py` initial migration.

*Note that this workflow will clear all existing entries in the database for your plugin's models!*

```shell
% invoke cli

/opt/nautobot/nautobot# python manage.py migrate nautobot_pluginname zero
Operations to perform:
  Unapply all migrations: nautobot_pluginname
Running migrations:
  Rendering model states... DONE
  Unapplying nautobot_pluginname.0001_initial... OK

/opt/nautobot/nautobot# rm /source/plugins/pluginname/nautobot_pluginname/migrations/0001_initial.py

/opt/nautobot/nautobot# python manage.py makemigrations nautobot_pluginname
Migrations for 'nautobot_pluginname':
  /source/plugins/pluginname/nautobot_pluginname/migrations/0001_initial.py
    - Create model MyModelName

/opt/nautobot/nautobot# python manage.py migrate nautobot_pluginname
Operations to perform:
  Apply all migrations: nautobot_pluginname
Running migrations:
  Applying nautobot_pluginname.0001_initial... OK

/opt/nautobot/nautobot# exit

% invoke restart
```

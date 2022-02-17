#!/bin/bash

set -e

cd /opt/nautobot
if [[ -e /opt/nautobot/plugin_requirements.txt ]] ; then
  echo "Setting up Nautobot plugins"
  pip install -r /opt/nautobot/plugin_requirements.txt
  nautobot-server post_upgrade
else
  echo "No plugins to set up"
fi

if [[ -e /opt/nautobot/plugin_config.py ]] ; then
  if ! grep -q "from plugin_config import *" /opt/nautobot/nautobot_config.py ; then
    echo "from plugin_config import *" >> /opt/nautobot/nautobot_config.py
  fi
fi

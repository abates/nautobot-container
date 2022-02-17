#!/bin/bash

set -e

if [[ -e /opt/nautobot/plugin_requirements.txt ]] ; then
  echo "Setting up Nautobot plugins"
  pip install -r /opt/nautobot/plugin_requirements.txt
  nautobot-server post_upgrade
else
  echo "No plugins to set up"
fi

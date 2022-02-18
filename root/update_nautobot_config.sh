#!/bin/bash

set -e

if [[ -e /opt/nautobot/plugin_config.py ]] ; then
  if ! grep -q "from plugin_config import *" /opt/nautobot/nautobot_config.py ; then
    tee -a /opt/nautobot/nautobot_config.py << END

plugin_file = os.path.join(NAUTOBOT_ROOT, "plugin_config.py")
if os.path.exists(plugin_file):
  try:
    import logging
    logger = logging.getLogger(__name__)
    logger.info("Loading plugin information from %s", plugin_file)
    sys.path.append(NAUTOBOT_ROOT)
    from plugin_config import *
  except Exception as e:
    # check to make sure that creating the logger wasn't
    # what raised the exception
    if logger:
      logger.warning("Failed to load plugins: %s", e)
END
  fi
fi

"""App declaration for Nautobot Deployment Tools."""
# Metadata is inherited from Nautobot. If not including Nautobot in the environment, this should be added
from importlib import metadata

from nautobot.apps import NautobotAppConfig

__version__ = metadata.version(__name__)


class NautobotDeploymentToolsConfig(NautobotAppConfig):
    """App configuration for the Nautobot Deployment Tools app."""

    name = "nautobot_deployment_tools"
    verbose_name = "Nautobot Deployment Tools"
    version = __version__
    author = "abates"
    description = "Collection of tools to help with Nautobot deployments."
    base_url = "deployment-tools"
    required_settings = []
    min_version = "2.0.0"
    max_version = "2.999"
    default_settings = {}
    caching_config = {}


config = NautobotDeploymentToolsConfig  # pylint:disable=invalid-name
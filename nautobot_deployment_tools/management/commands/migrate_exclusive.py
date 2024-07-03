"""Configure permissions on the instance."""

from django.core.cache import cache
from django.core.management import call_command
from django.core.management.base import BaseCommand

CACHE_MUTEX_KEY = "deployment-tools-exclusive-lock"



class Command(BaseCommand):
    """Run the migrate command, but with a lock.
    
    This command is the same as `nautobot-server migrate` except that
    prior to actually running the migration command a cache lock is obtained
    that prevents parallel processes from all trying to run the
    migrations at the same time. This helps to prevent database contention.
    """
    def handle(self, *args, **options):
        """Handle the execution of the command."""
        with cache.lock(CACHE_MUTEX_KEY):
            call_command("migrate")

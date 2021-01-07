import os

from django.contrib.auth import get_user_model

from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Creates an admin user non-interactively if it doesn't exist"

    def handle(self, *args, **options):
        user = get_user_model()
        if not user.objects.filter(username=os.getenv("DJANGO_SUPERUSER_USERNAME")).exists():
            call_command("createsuperuser", interactive=False)

import os

from django.contrib.auth import get_user_model
from django.core.management import call_command, BaseCommand

from main.utils import colored_print as _print


class Command(BaseCommand):
    help = "Runs base Django commands for project preparation"

    def handle(self, *args, **options):
        _print("Running migrations.", string_code="info", path="initialize")

        try:
            call_command("makemigrations", interactive=False)
            call_command("migrate", interactive=False)
        except Exception as exc:
            _print(str(exc), string_code="err", path="initialize")
            _print("Migrations failed.", string_code="err", path="initialize", exit=True)

        _print("Migrations passed successfully.", string_code="success", path="initialize")
        _print("Running collectstatic.", string_code="info", path="initialize")

        try:
            call_command("collectstatic", interactive=False)
        except Exception as exc:
            _print(str(exc), string_code="err", path="initialize")
            _print("Collect static files failed.", string_code="err", path="initialize", exit=True)

        _print("Static files were collect successfully.", string_code="success", path="initialize")

        user_model = get_user_model()
        superuser_username = os.getenv("DJANGO_SUPERUSER_USERNAME", "admin")
        superuser = user_model.objects.filter(username=superuser_username).first()

        if not superuser:
            _print("Creating superuser.", string_code="info", path="initialize")

            try:
                call_command("createsuperuser", interactive=False)
            except Exception as exc:
                _print(str(exc), string_code="warn", path="initialize")
                _print("Superuser creation failed.", string_code="warn", path="initialize")
            else:
                _print("Superuser created successfully.", string_code="success", path="initialize")
        else:

            try:
                superuser_password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "admin")
                superuser.set_password(superuser_password)
                superuser.save()
            except Exception as exc:
                _print(str(exc), string_code="warn", path="initialize")
                _print("Superuser password changing failed.", string_code="warn", path="initialize")
            else:
                _print("Superuser already exists. His password has changed.", string_code="info", path="initialize")

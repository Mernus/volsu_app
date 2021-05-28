import random

from django.core.management import BaseCommand

from event_manager.utils import colored_print as _print
from main.models import Event, Tag
from main.test.event_test_data import events
from main.test.tag_test_data import tags


class Command(BaseCommand):
    help = "Generate some tests data for project"

    def handle(self, *args, **options):
        _print("Running tags creation.", string_code="info", path="generate_test_data")

        tag_ids = []
        if Tag.objects.filter(title=tags[0]['title']).count() == 0:
            try:
                for tag_kwargs in tags:
                    obj = Tag.objects.create(**tag_kwargs)
                    tag_ids.append(obj.id)
            except Exception as exc:
                _print(str(exc), string_code="err", path="generate_test_data")
                _print("Tag creation failed.", string_code="err", path="generate_test_data", critical=True)

        _print("Tags created.", string_code="success", path="generate_test_data")

        _print("Running events creation.", string_code="info", path="generate_test_data")

        if Event.objects.filter(title=events[0]['title']).count() == 0:
            try:
                for event_kwargs in events:
                    obj = Event.objects.create(**event_kwargs)

                    ids_num = random.randint(1, 7)
                    obj.tags.add(*random.sample(tag_ids, ids_num))

            except Exception as exc:
                _print(str(exc), string_code="err", path="generate_test_data")
                _print("Event creation failed.", string_code="err", path="generate_test_data", critical=True)

        _print("Events created.", string_code="success", path="generate_test_data")
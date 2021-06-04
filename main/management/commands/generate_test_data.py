import random
from os import listdir
from os.path import join
from typing import List

from django.core.files import File
from django.core.management import BaseCommand

from event_manager.settings import BASE_DIR, MINIO_TEST_IMAGES
from event_manager.utils import colored_print as _print

from main.models import Event, EventFile, Tag, User
from main.test.event_test_data import EVENT_FILE_MAPPING, TEST_DIR, events
from main.test.tag_test_data import tags


def get_event_files(event_key: str) -> List['File']:
    if event_key not in EVENT_FILE_MAPPING:
        return []

    event_dir = join(TEST_DIR, MINIO_TEST_IMAGES, EVENT_FILE_MAPPING[event_key])
    event_files = []
    try:
        for ev_file in listdir(event_dir):
            event_files.append(EventFile(File(open(join(event_dir, ev_file), 'rb'))))
        return event_files
    except FileNotFoundError:
        return []


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
                    files = event_kwargs.pop('event_files')
                    obj = Event.objects.create(**event_kwargs)
                    for file in files:
                        event_file = EventFile.objects.create(event=obj)
                        event_file.file = file
                        event_file.save()

                    ids_num = random.randint(1, 7)
                    obj.tags.add(*random.sample(tag_ids, ids_num))

            except Exception as exc:
                _print(str(exc), string_code="err", path="generate_test_data")
                _print("Event creation failed.", string_code="err", path="generate_test_data", critical=True)

        _print("Events created.", string_code="success", path="generate_test_data")

        _print("Running user creation.", string_code="info", path="generate_test_data")

        try:
            # Add image to superuser
            superuser = User.objects.filter(is_superuser=True).first()
            profile_image = join(BASE_DIR, 'main/test', MINIO_TEST_IMAGES, 'users/superuser_image.jpg')
            superuser.profile_img.save('superuser_image.jpg', File(open(profile_image, 'rb')))

        except Exception as exc:
            _print(str(exc), string_code="err", path="generate_test_data")
            _print("User creation failed.", string_code="err", path="generate_test_data", critical=True)

        _print("User created.", string_code="success", path="generate_test_data")

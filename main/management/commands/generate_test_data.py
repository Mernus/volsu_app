import random
from os.path import join

from annoying.functions import get_object_or_None
from django.core.files import File
from django.core.management import BaseCommand

from event_manager.settings import BASE_DIR, MINIO_TEST_IMAGES
from event_manager.utils import colored_print as _print

from main.models import Event, EventFile, Tag, User
from main.test.event_test_data import events
from main.test.tag_test_data import tags


class Command(BaseCommand):
    help = "Generate some tests data for project"

    def handle(self, *args, **options):
        _print("Running tags creation.", string_code="info", path="generate_test_data")

        tag_ids = []
        try:
            for tag_kwargs in tags:
                title = tag_kwargs.get('title')

                obj = get_object_or_None(Tag, title=title)
                if obj is None:
                    obj = Tag.objects.create(**tag_kwargs)

                tag_ids.append(obj.id)
        except Exception as exc:
            _print(str(exc), string_code="err", path="generate_test_data")
            _print("Tag creation failed.", string_code="err", path="generate_test_data", critical=True)

        _print("Tags created.", string_code="success", path="generate_test_data")

        _print("Running events creation.", string_code="info", path="generate_test_data")

        try:
            for event_kwargs in events:
                files = event_kwargs.pop('event_files')
                title = event_kwargs.get('title')

                obj = get_object_or_None(Event, title=title)
                if obj is None:
                    obj = Event.objects.create(**event_kwargs)

                if obj.eventfile_set.count() == 0:
                    for file in files:
                        EventFile.objects.create(event=obj, file=file.get('file'), is_primary=file.get('is_primary'))

                if obj.tags.count() == 0:
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

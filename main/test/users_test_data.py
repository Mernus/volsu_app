from os.path import join
from pathlib import Path
from typing import Dict, Optional, Union

from django.core.files import File

from event_manager.settings import MINIO_TEST_IMAGES
from main.models import USER_LEVELS, User

superuser = User.objects.filter(is_superuser=True).first()

# Mapping to directories with test images
USER_PROFILE_MAPPING = {
    'test1': "users/test1/profile_img.jpeg",
    'test2': "users/test2/profile_img.jpg",
    'test3': "users/test3/profile_img.png",
    'test4': "users/test4/profile_img.png",
}

# Directory with test data
TEST_DIR = Path(__file__).absolute().parent


# TODO docs
def get_user_profile_img(username: str) -> Optional[Dict[str, Union[str, 'File']]]:
    if username not in USER_PROFILE_MAPPING:
        return None

    profile_img_path = join(TEST_DIR, MINIO_TEST_IMAGES, USER_PROFILE_MAPPING[username])
    try:
        file = File(open(profile_img_path, 'rb'))
        return {'filename': file.name, 'file': file}
    except FileNotFoundError:
        return None


user_01 = {
    'username': "test1",
    'password': "test1",
    'organization': "Test Organization",
    'email': "test1@mail.ru",
    'profile_img': get_user_profile_img('test1'),
}

user_02 = {
    'username': "test2",
    'password': "test2",
    'email': "test2@gmail.com",
    'level': USER_LEVELS.MODERATOR,
    'is_staff': True,
    'profile_img': get_user_profile_img('test2'),
}

user_03 = {
    'username': "test3",
    'password': "test3",
    'organization': "Test Organization v2",
    'email': "test3_the_best@volsu.ru",
    'profile_img': get_user_profile_img('test3'),
}

user_04 = {
    'username': "test4",
    'password': "test4",
    'email': "test-4@volsu.kz",
    'level': USER_LEVELS.ORGANIZER,
    'profile_img': get_user_profile_img('test4'),
}

users = [user_01, user_02, user_03, user_04]

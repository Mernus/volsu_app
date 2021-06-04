from annoying.functions import get_object_or_None
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

from event_manager.settings import MINIO_STORAGE_ENDPOINT, MINIO_STORAGE_MEDIA_BUCKET_NAME
from event_manager.settings.security import LOGIN_URL, LOGOUT_URL, SIGNUP_URL
from main.models import User

NO_AUTH_URLS = [
    LOGIN_URL, SIGNUP_URL, LOGOUT_URL,
    "/api/events/", "/api/tag/"
]

REQUIRED_AUTH_URLS = [
    "/api/event/", "/api/tag/",
    "/api/tag/update/", "/api/tag/create/",
    "/api/tag/delete/", "/api/settings/",
]


class TokenHeaderMiddleware(MiddlewareMixin):
    @staticmethod
    def _build_minio_uri(relative_uri: str):
        return f"{MINIO_STORAGE_ENDPOINT}/{MINIO_STORAGE_MEDIA_BUCKET_NAME}/{relative_uri}"

    def process_request(self, request):
        uri = request.META['REQUEST_URI']
        if uri in NO_AUTH_URLS:
            return None

        if "admin" not in uri and not any(url in uri for url in REQUIRED_AUTH_URLS):
            return redirect("api:events")

        user = request.user
        request.data['profile_img'] = self._build_minio_uri(user.profile_img)

        user_id = request.session.get('user_id')
        if user is None and user_id is not None:
            request.user = get_object_or_None(User, id=user_id)

        if not user.is_authenticated:
            return redirect(LOGIN_URL)

        access_token = request.session.get('jwt_access')
        if access_token:
            request.META['HTTP_AUTHORIZATION'] = f"Bearer {access_token}"
        return None

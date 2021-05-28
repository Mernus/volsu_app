from annoying.functions import get_object_or_None
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

from event_manager.settings.security import LOGIN_URL, LOGOUT_URL, SIGNUP_URL
from main.models import User

NO_AUTH_URLS = [
    LOGIN_URL, SIGNUP_URL, LOGOUT_URL,
    "/api/events/", "/api/tag/"
]

REQUIRED_AUTH_URLS = [
    "/api/event/", "/api/tag/", "/api/settings/",
]


class TokenHeaderMiddleware(MiddlewareMixin):
    def process_request(self, request):
        uri = request.META['REQUEST_URI']
        if uri in NO_AUTH_URLS:
            return

        if "admin" not in uri and not any(url in uri for url in REQUIRED_AUTH_URLS):
            return redirect("api:events")

        user = request.user
        user_id = request.session.get('user_id')
        if user is None and user_id is not None:
            request.user = get_object_or_None(User, id=user_id)

        if not request.user.is_authenticated:
            return redirect(LOGIN_URL)

        access_token = request.session.get('jwt_access')
        # raise Exception(request.session.get('jwt_access'))
        if access_token:
            request.META['HTTP_AUTHORIZATION'] = f"Bearer {access_token}"
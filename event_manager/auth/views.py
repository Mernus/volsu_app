import pytz
from django.contrib.auth import logout
from django.shortcuts import redirect

from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from event_manager.auth.serializers import LoginSerializer, RegistrationSerializer
from main.views.mixins import BaseSessionPopMixin


class RegistrationAPIView(APIView, BaseSessionPopMixin):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    renderer_classes = (TemplateHTMLRenderer,)
    serializer_errors = [
        'username_errors', 'password_errors',
        'timezone_errors', 'email_errors',
        'user_creation_errors'
    ]

    def post(self, request):
        serializer = self.serializer_class(data=request.data, request=request)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError:
            return redirect('registration')

        return redirect('/api/events')

    def get(self, request):
        access_token = request.session.get('jwt_access')
        if access_token is not None:
            self.session_pop(request)
            return redirect('/api/events')

        data = {error_name: request.session.get(error_name) for error_name in self.serializer_errors}
        data['timezones'] = pytz.common_timezones
        self.session_pop(request)

        return Response(data, template_name='auth/registration.html')


registration_page = RegistrationAPIView.as_view()


class LoginAPIView(APIView, BaseSessionPopMixin):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    renderer_classes = (TemplateHTMLRenderer,)
    serializer_errors = [
        'username_or_email_errors', 'password_errors',
        'nouser_errors', 'deactivated_user_errors',
    ]

    def post(self, request):
        serializer = self.serializer_class(data=request.data, request=request)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError:
            return redirect('login')

        return redirect('/api/events')

    def get(self, request):
        access_token = request.session.get('jwt_access')
        if access_token is not None:
            self.session_pop(request)
            return redirect('/api/events')

        data = {error_name: request.session.get(error_name) for error_name in self.serializer_errors}
        self.session_pop(request)

        return Response(data, template_name='auth/login.html')


login_page = LoginAPIView.as_view()


def logout_page(request):
    def session_pop(errors, request):
        for error_name in errors:
            request.session.pop(error_name, None)

    serializer_errors = [
        'nouser_errors', 'deactivated_user_errors',
    ]
    session_pop(serializer_errors, request)

    logout(request)
    return redirect('api:events')

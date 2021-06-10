import pytz

from rest_framework import mixins
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from main.models import User
from main.permissions import IsCurrentUser
from main.serializers import PasswordSerializer, UserSettingsSerializer


class SettingsViewSet(mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      GenericViewSet):
    queryset = User.objects.all()
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    serializer_class = UserSettingsSerializer
    permission_classes = [IsAuthenticated, IsCurrentUser]
    serializer_errors = [
        'nouser_errors', 'deactivated_user_errors',
    ]

    def retrieve(self, request, *args, **kwargs):
        response = super(SettingsViewSet, self).retrieve(request, *args, **kwargs)

        response.data['timezones'] = pytz.common_timezones
        response.template_name = 'user/settings.html'
        return response


get_settings = SettingsViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update'
})


class PasswordViewSet(APIView):
    queryset = User.objects.all()
    serializer_class = PasswordSerializer
    permission_classes = [IsAuthenticated, IsCurrentUser]
    serializer_errors = [
        'nouser_errors', 'deactivated_user_errors',
    ]

    def post(self, request):
        serializer = self.serializer_class(data=request.data, request=request)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError:
            return Response(serializer.errors)

        return Response(serializer.data)


update_password = PasswordViewSet.as_view()

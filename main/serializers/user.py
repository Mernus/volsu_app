from django.contrib.auth import authenticate, login
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers

from event_manager.auth import TimezoneField
from main.models import USER_LEVELS, User
from main.serializers.mixins import DateTimeFieldWihTZ


class EventUserSerializer(serializers.ModelSerializer):
    image = serializers.URLField(source='profile_img.url')

    class Meta:
        model = User
        fields = [
            "username", "image",
            "organization",
        ]
        read_only_fields = [
            "username", "image",
            "organization",
        ]


class UserSettingsSerializer(serializers.ModelSerializer):
    level_name = serializers.ChoiceField(source='get_level_display', choices=USER_LEVELS)
    added_aware = DateTimeFieldWihTZ(source='added', read_only=True)
    updated_aware = DateTimeFieldWihTZ(source='updated', read_only=True)
    last_login_aware = DateTimeFieldWihTZ(source='last_login', read_only=True)
    timezone = TimezoneField()

    def __init__(self, *args, **kwargs):
        self.request = kwargs['context'].pop('request')
        super(UserSettingsSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = [
            "username", "fullname",
            "organization", "added_aware",
            "updated_aware", "timezone", "email",
            "profile_img", "level_name", "last_login_aware"
        ]
        read_only_fields = [
            "level_name", "added_aware",
            "updated_aware", "last_login_aware"
        ]


class PasswordSerializer(serializers.Serializer):
    username_validator = UnicodeUsernameValidator()
    username = serializers.CharField(validators=[username_validator], max_length=80)
    old_password = serializers.CharField(max_length=128, write_only=True)
    new_password = serializers.CharField(max_length=128, write_only=True)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(PasswordSerializer, self).__init__(*args, **kwargs)

    def validate(self, data):
        username = data.get('username', None)
        old_password = data.get('old_password', None)
        new_password = data.get('new_password', None)

        user = authenticate(self.request, username=username, password=old_password)

        if user is None:
            raise serializers.ValidationError("Password is not valid")

        if not user.is_active:
            raise serializers.ValidationError("This user has been deactivated")

        user.set_password(new_password)
        user.save()

        login(self.request, user)
        token = user.get_token(new_password, self.request)
        self.request.session['user_id'] = user.id

        return {
            'user': user,
            'email': user.email,
            'username': user.username,
            'token': token
        }

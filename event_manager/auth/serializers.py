from django.contrib.auth import authenticate, login
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db.models import Q

from annoying.functions import get_object_or_None
from pytz import timezone as tz
from rest_framework import serializers
from rest_framework.fields import Field

from main.models import User


class TimezoneField(Field):
    """
    Custom field for serialize timezone objects, because by default drf doesn't contains it
    """
    default_error_messages = {
        'invalid': 'Not a valid timezone string representation.',
    }

    def to_internal_value(self, data):
        if not isinstance(data, str):
            self.fail('invalid')

        return tz(data)

    def to_representation(self, value):
        return value.zone


class RegistrationSerializer(serializers.Serializer):
    username_validator = UnicodeUsernameValidator()
    username = serializers.CharField(validators=[username_validator], max_length=80)
    password = serializers.CharField(max_length=128, write_only=True)
    timezone = TimezoneField()
    email = serializers.EmailField()

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(RegistrationSerializer, self).__init__(*args, **kwargs)

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)
        timezone = data.get('timezone', None)
        email = data.get('email', None)

        if username is None:
            self.request.session['username_errors'] = "An username isn't passed or not valid"

        if password is None:
            self.request.session['password_errors'] = "A password isn't passed or not valid"

        if timezone is None:
            self.request.session['timezone_errors'] = "A timezone isn't passed or not valid"

        if email is None:
            self.request.session['email_errors'] = "An email isn't passed or not valid"

        if username is None or password is None or timezone is None or email is None:
            raise serializers.ValidationError("Not all parameters passed or some is not valid")

        existed_users = User.objects.filter(Q(username=username) | Q(email=email)).cache()
        username_match = existed_users.filter(username=username).count()
        if username_match > 0:
            self.request.session['username_errors'] = "User with this username is already exists"
            raise serializers.ValidationError("User with this username is already exists")

        mail_match = existed_users.filter(email=email).count()
        if mail_match > 0:
            self.request.session['email_errors'] = "User with this email is already exists"
            raise serializers.ValidationError("User with this email is already exists")

        try:
            user = User.objects.create(**data)
        except (ValueError, TypeError) as exc:
            self.request.session['user_creation_errors'] = "Error while user creation"
            raise serializers.ValidationError(f"UserCreateError({type(exc)}): {str(exc)}")

        login(self.request, user)
        token = user.get_token(data['password'], self.request)
        self.request.session['user_id'] = user.id
        self.request.session['username'] = user.username

        return {
            'user': user,
            'email': user.email,
            'username': user.username,
            'token': token
        }


class LoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField(max_length=254, allow_blank=True)
    password = serializers.CharField(max_length=128, write_only=True, allow_blank=True)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(LoginSerializer, self).__init__(*args, **kwargs)

    def validate(self, data):
        username_or_email = data.get('username_or_email', None)
        password = data.get('password', None)

        if username_or_email is None:
            self.request.session['username_or_email_errors'] = "An email or username isn't passed or not valid"

        if password is None:
            self.request.session['password_errors'] = "A password isn't passed or not valid"

        if username_or_email is None or password is None:
            raise serializers.ValidationError(
                "An email or username and password isn't passed or not valid"
            )

        user = get_object_or_None(User, email=username_or_email)
        if user is not None:
            username_or_email = user.username

        user = authenticate(self.request, username=username_or_email, password=password)

        if user is None:
            self.request.session['nouser_errors'] = "A user with this email and password was not found"
            raise serializers.ValidationError(
                "A user with this email and password was not found"
            )

        if not user.is_active:
            self.request.session['deactivated_user_errors'] = "This user has been deactivated"
            raise serializers.ValidationError(
                "This user has been deactivated"
            )

        login(self.request, user)
        token = user.get_token(password, self.request)
        self.request.session['user_id'] = user.id
        self.request.session['username'] = user.username

        return {
            'user': user,
            'email': user.email,
            'username': user.username,
            'token': token
        }

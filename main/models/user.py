from django.contrib.auth import password_validation
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db import models

from django_cryptography.fields import encrypt
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField
from model_utils import Choices
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import TokenBackendError, TokenError
from timezone_field import TimeZoneField

from main.utils import get_tokens
from main.exceptions import TokenAuthError
from main.validators import FullnameValidator, TitleValidator

USER_LEVELS = Choices(
    (0, 'USER', 'Пользователь'),
    (1, 'ORGANIZER', 'Организатор'),
    (2, 'MODERATOR', 'Модератор'),
    (3, 'ADMIN', 'Администратор'),
)


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-level', 'username']

    username_validator = UnicodeUsernameValidator()
    org_validator, fullname_validator = TitleValidator(), FullnameValidator()

    username = models.CharField(verbose_name='Имя пользователя', validators=[username_validator],
                                max_length=80, unique=True)
    fullname = encrypt(models.CharField(verbose_name='ФИО пользователя', validators=[fullname_validator],
                                        max_length=30, unique=True, null=True, blank=True))
    organization = encrypt(models.CharField(verbose_name='Организация', max_length=120,
                                            validators=[org_validator], null=True, blank=True))
    added = CreationDateTimeField(verbose_name='Дата создания')
    updated = ModificationDateTimeField(verbose_name='Дата последнего изменения')
    timezone = TimeZoneField(default='Europe/Moscow', verbose_name="Часовой пояс")
    email = encrypt(models.EmailField(verbose_name='Почта пользователя', unique=True))
    level = models.IntegerField(verbose_name='Уровень прав пользователя',
                                choices=USER_LEVELS,
                                default=USER_LEVELS.USER)
    is_staff = models.BooleanField('Может использовать админ сайт', default=False)
    is_active = models.BooleanField('Активен',
                                    default=True,
                                    help_text='Активен ли пользователь. Используется вместо удаления объекта.')

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    # TODO docs
    @property
    def token(self, password=None):
        return self.__generate_token(password)

    # TODO docs
    def save(self, *args, **kwargs):
        super(AbstractBaseUser, self).save(*args, **kwargs)
        if self._password is not None:
            self.__generate_token(self._password)
            password_validation.password_changed(self._password, self)
            self._password = None

    # TODO docs
    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

        if self.level is USER_LEVELS.ORGANIZER:
            if not self.organization:
                self.organization = 'Без организации'
        elif self.organization:
            raise ValidationError(
                {'organization': 'Организация может быть только у пользователя с правами Организатор'}
            )

        self.is_staff = self.level is USER_LEVELS.ADMIN

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_full_name(self):
        return f'{self.username}: {self.level}'

    def get_short_name(self):
        return self.username

    # TODO docs
    def __generate_token(self, raw_password: str) -> str:
        username, email = self.username, self.email
        try:
            data = get_tokens(username, raw_password)
        except (AuthenticationFailed, TokenError, TokenBackendError) as e:
            raise TokenAuthError(username, email, str(e))

        access_token = data['access']
        cache_data = {'jwt_access': access_token}

        refresh_token = data.get('refresh')
        if refresh_token is not None:
            cache_data['jwt_refresh'] = refresh_token

        cache.set_many(cache_data)
        return access_token

    def __str__(self):
        return self.get_full_name()

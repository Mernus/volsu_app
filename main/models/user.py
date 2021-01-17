from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator

from django.core.exceptions import ValidationError
from django.core.mail import send_mail

from django.db import models

from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField
from model_utils import Choices
from timezone_field import TimeZoneField

from main.validators import FullnameValidator

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
    fullname_validator = FullnameValidator()

    username = models.CharField(verbose_name='Имя пользователя', validators=[username_validator],
                                max_length=30, unique=True)
    fullname = models.CharField(verbose_name='ФИО пользователя', validators=[fullname_validator], max_length=30,
                                unique=True, null=True, blank=True)
    organization = models.CharField(verbose_name='Организация', max_length=120,
                                    null=True, blank=True)
    added = CreationDateTimeField(verbose_name='Дата создания')
    updated = ModificationDateTimeField(verbose_name='Дата последнего изменения')
    timezone = TimeZoneField(default='Europe/Moscow', verbose_name="Часовой пояс")
    email = models.EmailField(verbose_name='Почта пользователя', unique=True,
                              blank=True, null=True)
    level = models.IntegerField(verbose_name='Уровень прав пользователя',
                                choices=USER_LEVELS,
                                default=USER_LEVELS.USER)
    is_staff = models.BooleanField('Может использовать админ сайт', default=False)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

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

    def __str__(self):
        return self.get_full_name()

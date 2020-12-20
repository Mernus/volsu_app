from django.db import models

from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField
from model_utils import Choices
from timezone_field import TimeZoneField

ACCOUNT_LEVELS = Choices(
    (0, 'DEFAULT', 'Пользователь'),
    (1, 'ORGANIZER', 'Организатор'),
    (2, 'ADMIN', 'Администратор'),
)


class Account(models.Model):
    class Meta:
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'
        ordering = ['-level', 'name']

    name = models.CharField(verbose_name='Имя аккаунта', max_length=64, unique=True)
    shortname = models.CharField(verbose_name='Короткое имя аккаунта', max_length=3, unique=True)
    added = CreationDateTimeField(verbose_name='Дата создания')
    updated = ModificationDateTimeField(verbose_name='Дата последнего изменения')
    timezone = TimeZoneField(default='Europe/Moscow', verbose_name="Часовой пояс")
    level = models.IntegerField(verbose_name='Уровень прав аккаунта',
                                choices=ACCOUNT_LEVELS,
                                default=ACCOUNT_LEVELS.DEFAULT)

    def __str__(self):
        return f'{self.name}: {self.level}'

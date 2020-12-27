from django.contrib.postgres.fields import CICharField

from colorfield.fields import ColorField
from django_extensions.db.models import TimeStampedModel

from .event import Event


def get_popular_tags():
    return Tag.objects.order_by('events_num')


class Tag(TimeStampedModel):
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['title']

    title = CICharField(verbose_name='Тег', max_length=50, unique=True)
    back_color = ColorField(verbose_name='Цвет бэкграунда тега', default='#FFFFFF')
    title_color = ColorField(verbose_name='Цвет тега', default='#000000')

    def __str__(self):
        return self.title

    @property
    def events_num(self):
        return Event.objects.filter(tags=self)

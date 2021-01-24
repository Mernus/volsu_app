from django.contrib.postgres.fields import CICharField

from colorfield.fields import ColorField
from django_extensions.db.models import TimeStampedModel

from main.models import Event
from main.validators import TitleValidator


# TODO озаботиться кешированием(обновлять в случае добавления/удаления тегов к какому-то евенту)
def get_popular_tags():
    return Tag.objects.order_by('events_num')[:10]


class Tag(TimeStampedModel):
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['title']

    title_validator = TitleValidator()

    title = CICharField(verbose_name='Тег', validators=[title_validator],
                        max_length=50, unique=True)
    back_color = ColorField(verbose_name='Цвет бэкграунда тега', default='#FFFFFF')
    title_color = ColorField(verbose_name='Цвет тега', default='#000000')

    def __str__(self):
        return self.title

    # TODO добавить кеширование результатов(обновлять в случае добавления/удаления тега к ивенту)
    @property
    def events_num(self):
        return Event.objects.filter(tags=self).count()

from django.contrib.postgres.fields import CICharField
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.utils.functional import cached_property, classproperty

from colorfield.fields import ColorField
from django_extensions.db.models import TimeStampedModel

from main.models import Event
from main.utils import clear_cached_properties
from main.validators import TitleValidator


TAG_CACHED_PROPERTIES = {
    "events_num"
}


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

    # TODO озаботиться кешированием(обновлять в случае добавления/удаления тегов к какому-то ивенту)
    @classproperty
    def get_popular_tags(self):
        """
        Cached class property that calculates 10 most popular Tags.

        Returns:
            (list): list of 10 popular tags

        """
        return sorted(Tag.objects.all(), key=lambda tag: tag.events_num, reverse=True)[:10]

    @cached_property
    def events_num(self):
        """
        Cached object property that calculates num of events with this Tag.

        Returns:
            (int): num of events with this tag

        """
        return Event.objects.filter(tags=self).count()


@receiver(m2m_changed, sender=Event.tags.through)
def clear_tag_cache(sender, instance: Event, **kwargs: dict):
    """
    Clear Tags cached property, when any Tag added or removed from any Event.

    Args:
        sender (ModelBase): Event tags class
        instance (Event): Event instance with changed tags field
        **kwargs (dict): Provided info as signal, action and other

    Returns:

    """

    # Clear cached properties that had this tag
    clear_cached_properties(instance, TAG_CACHED_PROPERTIES)

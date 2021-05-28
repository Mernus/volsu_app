from django.contrib.postgres.fields import CICharField
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.utils.functional import cached_property

from colorfield.fields import ColorField
from django_extensions.db.models import TimeStampedModel

from main.models.event import Event
from event_manager.utils import clear_cached_properties
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
                        max_length=20, unique=True)
    back_color = ColorField(verbose_name='Цвет бэкграунда тега', default='#000000')
    title_color = ColorField(verbose_name='Цвет тега', default='#FFFFFF')

    def __str__(self):
        return self.title

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
    """

    # Clear cached properties that had this tag
    clear_cached_properties(instance, TAG_CACHED_PROPERTIES)

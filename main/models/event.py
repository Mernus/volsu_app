import re
import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.utils import timezone
from django.utils.functional import cached_property

from django_cryptography.fields import encrypt
from django_extensions.db.fields import AutoSlugField
from django_extensions.db.models import TimeStampedModel
from model_utils import Choices, FieldTracker
from model_utils.managers import QueryManager

from event_manager.utils import clear_cached_properties
from main.utils import render_tags
from main.validators import TitleValidator

EVENT_CACHED_PROPERTIES = {
    "get_popular_tags", "get_tags_html"
}

# Statuses for Events that are not represented for default users, only for author of the Event and Moderators, Admins
NONPUBLIC_EVENT_STATUSES = Choices(
    (0, 'RECONCILIATION', 'Reconciliation'),
    (-1, 'REJECTED', 'Rejected'),
)

# Statuses for Events that are represented for all users
PUBLIC_EVENT_STATUSES = Choices(
    (1, 'WAITING', 'Waiting for start'),
    (2, 'INPROCESS', 'In process'),
    (3, 'PASSED', 'Already passed'),
)

# Statuses for all events
EVENT_STATUSES = NONPUBLIC_EVENT_STATUSES + PUBLIC_EVENT_STATUSES

# Fields which changes tracked by special field "changes"
TRACKED_FIELDS = [
    'title', 'description', 'author',
    'start_date', 'end_date', 'status'
]


def files_upload(instance: 'EventFile', filename: str):
    """
    Return path for uploaded files to minio

    Args:
        instance (EventFile): event instance
        filename (str): filename of the file

    Returns:
        str: file path in minio
    """
    match = re.search(r"\.[^.\\/:*?\"<>|\r\n]+$", filename)
    extension = match.group(0)
    result_filename = str(uuid.uuid4())
    return f"events/{instance.event.slug}/files/{result_filename}{extension}"


class EventFile(TimeStampedModel):
    class Meta:
        verbose_name = 'Файл события'
        verbose_name_plural = 'Файлы события'
        ordering = ['event']

    event = models.ForeignKey('Event', on_delete=models.CASCADE, verbose_name='Cобытие')
    file = models.FileField(upload_to=files_upload, verbose_name='Файл', null=True)


class Event(TimeStampedModel):
    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'
        ordering = ['start_date']

    title_validator = TitleValidator()

    title = models.CharField(verbose_name='Название события', validators=[title_validator],
                             max_length=100, unique=True)
    description = encrypt(models.TextField(verbose_name='Описание события', max_length=450, null=True, default=None))
    location = encrypt(models.CharField(verbose_name='Местоположение', max_length=300, null=True, default=None))
    website = models.CharField(verbose_name='Официальный вебсайт', max_length=150, null=True)
    slug = AutoSlugField(populate_from=['author', 'title'])
    tags = models.ManyToManyField('Tag', blank=True, verbose_name='Теги события')
    author = models.ForeignKey('User', blank=True, null=True,
                               on_delete=models.SET_NULL,
                               verbose_name='Организатор события')
    participants = models.ManyToManyField('User', blank=True,
                                          verbose_name='Участники события',
                                          related_name='participants')
    start_date = models.DateTimeField(verbose_name='Время и дата начала события', null=True, blank=True)
    end_date = models.DateTimeField(verbose_name='Время и дата конца события', null=True, blank=True)
    status = models.IntegerField(verbose_name='Статус события',
                                 choices=EVENT_STATUSES,
                                 default=EVENT_STATUSES.RECONCILIATION)

    objects = models.Manager()
    public_objects = QueryManager(author__isnull=False, status__in=[1, 2, 3])
    changes = FieldTracker(fields=TRACKED_FIELDS)  # Track changes in some fields

    def first_participants(self):
        return self.participants.all()[:4].values_list('profile_img', flat=True)

    @property
    def get_first_image_url(self) -> str:
        event_file = self.eventfile_set.first()
        return event_file.file.url if event_file else None

    @property
    def get_files_url(self) -> list[str]:
        return [event_file.file.url for event_file in self.eventfile_set.all() if event_file]

    @cached_property
    def get_popular_tags_html(self) -> list[str]:
        """
        Cached class property that calculates 5 most popular Tags form this event.

        Returns:
            (list): list of 5 popular tags
        """
        sorted_tags = sorted(self.tags.all(), key=lambda some_tag: some_tag.events_num, reverse=True)[:5]
        return render_tags(sorted_tags)

    @cached_property
    def get_tags_html(self) -> list[str]:
        """
        Cached class property that calculates most popular Tags form this event.

        Returns:
            (list): list of tags
        """
        sorted_tags = sorted(self.tags.all(), key=lambda some_tag: some_tag.events_num, reverse=True)
        return render_tags(sorted_tags)

    def save(self, **kwargs):
        """
        Overrides base save method to set event status depending on start and end dates.
        """

        now = timezone.now()
        if not self.start_date and not self.end_date:
            self.status = EVENT_STATUSES.RECONCILIATION

        elif self.end_date:
            if self.end_date < now:
                self.status = EVENT_STATUSES.PASSED
            elif self.start_date and self.start_date < now < self.end_date:
                self.status = EVENT_STATUSES.INPROCESS

        super(Event, self).save()

    @property
    def fullname(self):
        """
        Represent event as string.

        Returns:
            str: Event representation as string
        """
        author = f": {self.author}" if self.author else ""
        event_repr = f'{self.title}{author}'

        if self.start_date and self.end_date:
            event_repr += f'({self.start_date} - {self.end_date})'

        return event_repr

    def __str__(self):
        return self.fullname


@receiver(m2m_changed, sender=Event.tags.through)
def clear_event_cache(sender, instance: Event, **kwargs: dict):
    """
    Clear Events cached property, when any Tag added or removed from any Event.

    Args:
        sender (ModelBase): Event tags class
        instance (Event): Event instance with changed tags field
        **kwargs (dict): Provided info as signal, action and other
    """

    # Clear cached properties that had this tag
    clear_cached_properties(instance, EVENT_CACHED_PROPERTIES)


@receiver(m2m_changed, sender=Event.tags.through)
def check_tags_num(sender, instance: Event, **kwargs: dict):
    """
    Checks that tags number for events is lowered than 10.

    Args:
        sender (ModelBase): Event tags class
        instance (Event): Event instance with changed tags field
        **kwargs (dict): Provided info as signal, action and other
    """

    # Clear cached properties that had this tag
    if instance.tags.count() > 10:
        raise ValidationError("You can't assign more than ten Tags to Event")

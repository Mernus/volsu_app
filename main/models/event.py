from django.db import models
from django.utils import timezone

from django_extensions.db.fields import AutoSlugField
from django_extensions.db.models import TimeStampedModel
from model_utils import Choices, FieldTracker
from model_utils.managers import QueryManager

from main.validators import TitleValidator


# Statuses for Events that are not represented for default users, only for author of the Event and Moderators, Admins
NONPUBLIC_EVENT_STATUSES = Choices(
    (0, 'RECONCILIATION', 'На этапе согласования'),
    (-1, 'REJECTED', 'Отменено'),
)

# Statuses for Events that are represented for all users
PUBLIC_EVENT_STATUSES = Choices(
    (1, 'WAITING', 'Ожидается начало'),
    (2, 'INPROCESS', 'В процессе проведения'),
    (3, 'PASSED', 'Прошло'),
)

# Statuses for all events
EVENT_STATUSES = NONPUBLIC_EVENT_STATUSES + PUBLIC_EVENT_STATUSES

# Fields which changes tracked by special field "changes"
TRACKED_FIELDS = [
    'title', 'description', 'author',
    'start_date', 'end_date', 'status'
]


class Event(TimeStampedModel):
    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'
        ordering = ['start_date']

    title_validator = TitleValidator()

    title = models.CharField(verbose_name='Название события', validators=[title_validator],
                             max_length=100, unique=True)
    description = models.TextField(verbose_name='Описание события', max_length=450,
                                   blank=True, null=True)
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
    public_objects = QueryManager(author__isnull=False, status__in=PUBLIC_EVENT_STATUSES)
    changes = FieldTracker(fields=TRACKED_FIELDS)  # Track changes in some fields

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

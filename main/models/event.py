from django.db import models
from django.utils import timezone

from django_extensions.db.fields import AutoSlugField
from django_extensions.db.models import TimeStampedModel

from model_utils import Choices, FieldTracker
from model_utils.managers import QueryManager


NONPUBLIC_EVENT_STATUSES = Choices(
    (0, 'RECONCILIATION', 'На этапе согласования'),
    (-1, 'REJECTED', 'Отменено'),
)

PUBLIC_EVENT_STATUSES = Choices(
    (1, 'WAITING', 'Ожидается начало'),
    (2, 'INPROCESS', 'В процессе проведения'),
    (3, 'PASSED', 'Прошло'),
)

EVENT_STATUSES = NONPUBLIC_EVENT_STATUSES + PUBLIC_EVENT_STATUSES


class Event(TimeStampedModel):
    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'
        ordering = ['start_date']

    title = models.CharField(verbose_name='Название события', max_length=100, unique=True)
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
    changes = FieldTracker()
    
    def save(self, **kwargs):
        """
        Overrides base save method to set event status depending on start and end dates.

        """

        now = timezone.now()
        if self.end_date:
            if self.start_date and self.start_date < now < self.end_date:
                self.status = EVENT_STATUSES.INPROCESS
            elif self.end_date < now:
                self.status = EVENT_STATUSES.PASSED

        super(Event, self).save()

    @property
    def fullname(self):
        event_repr = f'{self.author}: {self.title}'
        if self.start_date and self.end_date:
            event_repr += f'({self.start_date} - {self.end_date})'

        return event_repr

    def __str__(self):
        return self.fullname

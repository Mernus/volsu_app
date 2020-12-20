from django.contrib.postgres.fields import CICharField

from django_extensions.db.models import TimeStampedModel


class Tag(TimeStampedModel):
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['title']

    title = CICharField(verbose_name='Тег', max_length=50, unique=True)

    def __str__(self):
        return self.title

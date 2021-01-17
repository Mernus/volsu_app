from django import forms
from django.contrib import admin

from main.models import Event


class EventAdminForm(forms.ModelForm):
    model = Event

    class Meta:
        exclude = ['slug']

    def clean(self) -> dict:
        """
        Validate the start and end dates of the event.

        Returns:
            dict: Cleaned data from request

        Raises:
            ValidationError: If the start date later than the end date

        """
        cleaned_data = super(EventAdminForm, self).clean()

        start = self.cleaned_data.get('start_date', None)
        end = self.cleaned_data.get('end_date', None)

        if start and end and start > end:
            raise forms.ValidationError(
                'Невозможно добавить событие. '
                'Дата начала события не может быть позже даты его конца.'
            )

        return cleaned_data


class EventAdmin(admin.ModelAdmin):
    form = EventAdminForm

    def author_fullname(self, obj: Event) -> str:
        """
        Returns event author if it exists.

        Args:
            obj (Event): Some event object

        Returns:
            string: Event author full name if exists otherwise returns a blank string

        """
        return obj.author.get_full_name() if obj.author else "---"

    author_fullname.admin_order_field = 'author__fullname'

    def event_tags(self, obj):
        """
        Returns list of event tags descending ordered by number of entries this tag in events.

        Args:
            obj (Event): Some event object

        Returns:
            list: Ordered event tags

        """
        return sorted(obj.tags.all(), key=lambda tag: tag.events_num, reverse=True)

    event_tags.admin_order_field = 'event__tags'

    date_hierarchy = 'start_date'
    readonly_fields = ('status',)
    list_display = ('title', 'author_fullname', 'status', 'event_tags')
    list_display_links = ('title',)
    radio_fields = {'status': admin.VERTICAL}
    list_filter = (
        ('author', admin.RelatedOnlyFieldListFilter),
        ('status', admin.ChoicesFieldListFilter),
        ('start_date', admin.DateFieldListFilter),
        ('tags', admin.RelatedOnlyFieldListFilter),
    )
    list_per_page = 10
    search_fields = ('title', 'author', 'start_date', 'end_date', 'tags')

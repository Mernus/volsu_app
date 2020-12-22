from django import forms
from django.contrib import admin
from django.utils import timezone

from main.models import Event, EVENT_STATUSES


class EventAdminForm(forms.ModelForm):
    model = Event

    class Meta:
        exclude = ['slug']

    def clean(self):
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

    def author_name(self, obj):
        return obj.author.name
    author_name.admin_order_field = 'author__name'

    date_hierarchy = 'start_date'
    readonly_fields = ('status',)
    list_display = ('title', 'author_name', 'start_date', 'end_date', 'status')
    list_display_links = ('title',)
    radio_fields = {'status': admin.VERTICAL}
    list_filter = (
        ('author', admin.RelatedOnlyFieldListFilter),
        ('status', admin.ChoicesFieldListFilter),
        ('start_date', admin.DateFieldListFilter)
    )
    list_per_page = 10
    search_fields = ('title', 'author_name', 'start_date', 'end_date')

    def save_model(self, request, obj, form, change):
        now = timezone.now()
        if obj.end_date:
            if obj.start_date and obj.start_date < now < obj.end_date:
                obj.status = EVENT_STATUSES.INPROCESS
            elif obj.end_date < now:
                obj.status = EVENT_STATUSES.PASSED

        super().save_model(request, obj, form, change)

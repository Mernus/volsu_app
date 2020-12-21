from django import forms
from django.contrib import admin
from django.utils import timezone

from main.models import Event


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
    date_hierarchy = 'start_date'
    readonly_fields = 'status'
    list_display = ('title', 'author', 'start_date', 'end_date', 'status')
    list_display_links = 'title'
    # list_filter = (
    #     'shortname',
    #     ('level', admin.ChoicesFieldListFilter)
    # )
    list_per_page = 10
    search_fields = ('title', 'author', 'start_date', 'end_date')

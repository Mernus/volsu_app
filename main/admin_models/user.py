from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultAdmin


# TODO переработать после обновы
class UserAdmin(DefaultAdmin):
    date_hierarchy = 'added'
    readonly_fields = ('added', 'updated')
    list_display = ('username', 'level', 'added')
    list_display_links = ('username',)
    radio_fields = {'level': admin.HORIZONTAL}
    list_filter = (
        ('level', admin.ChoicesFieldListFilter),
    )
    list_per_page = 20
    search_fields = ('username', 'fullname', 'level')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {'fields': ('fullname', 'timezone', 'email')}),
        ('Права', {
            'fields': ('organization', 'level', 'groups', 'user_permissions'),
        }),
        ('Техническая информация', {'fields': ('added', 'updated')}),
    )

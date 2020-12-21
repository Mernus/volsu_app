from django.contrib import admin


class AccountAdmin(admin.ModelAdmin):
    date_hierarchy = 'added'
    readonly_fields = ('added', 'updated')
    list_display = ('shortname', 'level', 'added')
    list_display_links = 'shortname'
    list_filter = (
        'shortname',
        ('level', admin.ChoicesFieldListFilter)
    )
    list_per_page = 20
    search_fields = ('shortname', 'level')

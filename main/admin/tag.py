from django.contrib import admin


class TagAdmin(admin.ModelAdmin):
    list_display = 'title'
    list_per_page = 50

from django.contrib import admin


class TagAdmin(admin.ModelAdmin):
    list_display = ('title', 'events_num', 'back_color', 'title_color')
    list_per_page = 50

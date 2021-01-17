from django.contrib import admin

from main.admin_models import UserAdmin, TagAdmin, EventAdmin
from main.models import User, Tag, Event

admin.site.register(User, UserAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Event, EventAdmin)

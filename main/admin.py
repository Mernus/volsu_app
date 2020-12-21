from django.contrib import admin

from main.admin import AccountAdmin, TagAdmin, EventAdmin
from main.models import Account, Tag, Event

admin.site.register(Account, AccountAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Event, EventAdmin)

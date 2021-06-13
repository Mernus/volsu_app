from django.contrib import admin
from django.urls import include, path

from event_manager.auth import login_page, logout_page, registration_page

urlpatterns = [
    # Auth URLs
    path('signup/', registration_page, name='registration'),
    path('login/', login_page, name='login'),
    path('logout/', logout_page, name='logout'),

    # Admin
    path('admin/', admin.site.urls),

    # RestFramework APIs
    path('api/', include('main.urls', namespace='api')),
]

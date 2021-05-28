from django.contrib import admin
from django.urls import include, path

from event_manager.auth import login_page, logout_page, registration_page

urlpatterns = [
    path('signup/', registration_page, name='registration'),
    path('login/', login_page, name='login'),
    path('logout/', logout_page, name='logout'),
    path('admin/', admin.site.urls),
    path('api/', include('main.urls', namespace='api')),
]

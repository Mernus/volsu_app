from django.contrib import admin
from django.urls import include, path

from main.views import index

urlpatterns = [
    path('', index),
    path('admin/', admin.site.urls),
    path('api/', include('main.urls', namespace='api')),
]

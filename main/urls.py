from django.urls import include, path

from rest_framework import routers

from main.views import UserViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls))
]

from django.urls import path

from main import views

app_name = 'api'

urlpatterns = [
    # Events
    path('events/', views.event_list, name='events'),
    path('event/<str:slug>/', views.event_detail, name='event_detail'),

    # Tags
    path('tag/', views.tag_list, name='tags'),
    path('tag/update/<int:pk>/', views.tag_part_update, name='tag_update'),
    path('tag/create/', views.tag_create, name='tag_create'),
    path('tag/delete/<int:pk>/', views.tag_delete, name='tag_delete'),

    # Settings
    path('settings/<int:pk>/', views.get_settings, name='settings'),
    path('settings/update_password/', views.update_password, name='settings'),
]

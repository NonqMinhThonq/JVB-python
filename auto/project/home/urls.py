from django.urls import path
from .views import home_view, logout_view, show_all_notifications

urlpatterns = [
    path('', home_view, name='home'),
    path('logout/', logout_view, name='logout'),
    path('notifications/', show_all_notifications, name='show_all_notifications'),
]
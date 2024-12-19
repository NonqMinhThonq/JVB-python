from django.contrib import admin
from django.urls import path, include
from login.detail_view.login_view import login_view
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view, name='login'),
    path('login/', include('login.urls')),
    path('home/', include('home.urls')),
    path('manage_university/', include('manage_university.urls')),
    path('student/', include('manage_student.urls')),
]

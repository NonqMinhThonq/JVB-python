from django.urls import path
from .detail_view.register_view import register_view
from .detail_view.login_view import login_view
from .detail_view.repassword_view import repassword_view
from .detail_view.forgot_view import forgot_view
urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('forgot/', forgot_view, name='forgot'),
    path('re-password/<str:username>/', repassword_view, name='repassword_view'),
]
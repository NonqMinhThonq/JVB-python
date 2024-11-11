from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

# Trang chính đơn giản để thử nghiệm
def home_view(request):
    return render(request, 'home.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),  # Liên kết đến ứng dụng 'accounts' nếu bạn có
    path('', home_view, name='home'),  # Trang chính
]

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
# Create your views here.
@login_required
def home_view(request):
    return render(request, 'home/home.html')  

from django.urls import reverse

def logout_view(request):
    logout(request)
    return redirect(reverse('login')) 


def show_all_notifications(request):
    notifications = request.session.get('notifications', [])
    return render(request, 'admin/all_notifications.html', {'notifications': notifications})

from django.shortcuts import redirect
from django.contrib.auth import login, logout
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import RegisterForm, LoginForm

class UserRegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('home')  # Chuyển hướng sau khi đăng ký thành công

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = 'login.html'
    redirect_authenticated_user = True  # Tự động chuyển hướng người dùng đã đăng nhập về 'home'
    next_page = reverse_lazy('home')    # Chuyển hướng sau khi đăng nhập thành công

def logout_view(request):
    logout(request)
    return redirect('login')  # Chuyển hướng về trang đăng nhập sau khi đăng xuất

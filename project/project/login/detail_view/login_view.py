from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
def login_view(request):
    if request.method == 'POST':
        # Lấy thông tin từ form
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, "Vui lòng điền đầy đủ thông tin.")
            return render(request, 'login/login.html')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home') 
        else:
            messages.error(request, "Tên tài khoản hoặc mật khẩu không đúng.")
            return render(request, 'login/login.html')
    return render(request, 'login/login.html')
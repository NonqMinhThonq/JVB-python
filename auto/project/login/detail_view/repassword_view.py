from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User

def repassword_view(request, username):
    if request.method == 'POST':
        password = request.POST.get('password')
        re_password = request.POST.get('re_password')
        if password != re_password:
            messages.error(request, 'Mật khẩu không khớp!')
            return redirect('repassword_view', username=username)
        if len(password) < 8:
            messages.error(request, 'Mật khẩu phải có ít nhất 8 ký tự!')
            return redirect('repassword_view', username=username)
        try:
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            messages.success(request, 'Đổi mật khẩu thành công!')
            return redirect('login')  # Quay lại trang đăng nhập
        except User.DoesNotExist:
            messages.error(request, 'Không tìm thấy người dùng này!')
            return redirect('repassword_view', username=username)
    return render(request, 'login/re-password.html', {'username': username})

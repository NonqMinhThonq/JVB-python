from django.shortcuts import render # tra ve 1 http response kem theo template html va du lieu cho nguoi dung
from django.shortcuts import redirect # dung de chuyen huong nguoi dung sang 1 url khac
from django.contrib import messages # tra va thong bao cho nguoi dung, nhung thong bao nay se hien owr template neu ban cau hinh
from django.contrib.auth.models import User # truong tac voi thong tin nguoi dung
import random # la 1 thu vien python de tao ra gia tri ngau nhien
import time # is a built- in python library for working with time
from common_service.otp import confirm
otp_storage = {}
def forgot_view(request):
    try:
        if request.method != 'POST':
            return render(request, 'login/forgot-password.html')
        else:
            username = request.POST.get('username')
            email = request.POST.get('email')
            action = request.POST.get('action')        
            if action == 'get_otp':
                if not username:
                    messages.error(request, 'Vui lòng nhập username')
                    return render(request, 'login/forgot-password.html')
                elif not email:
                    messages.error(request, "Vui lòng nhập email.")
                    return render(request, 'login/forgot-password.html')
                try:
                    user = User.objects.get(username=username, email=email)
                except User.DoesNotExist:
                    messages.error(request, "Không tìm thấy tài khoản với tên đăng nhập hoặc email này.")
                    return render(request, 'login/forgot-password.html')
                # xoa otp cu neu co
                if username in otp_storage:
                    del otp_storage[username]
                otp = f'{random.randint(0, 9999):04}'
                otp_storage[username] = {'otp': otp, 'timestamp': time.time()}
                try:
                    title = 'Xác nhận thông tin'
                    content = f'Mã xác nhận của bạn là {otp}'
                    confirm(email, title, content)
                    messages.success(request, "OTP đã được gửi đến email của bạn, OTP chỉ có hiệu lực trong vòng 5 phút.")
                    return render(request, 'login/forgot-password.html')
                except Exception as e:
                    messages.error(request, f"Không thể gửi email: {e}")
                    return render(request, 'login/forgot-password.html')
                
            if action == 'reset_password':
                input_otp = request.POST.get('otp')
                # Kiểm tra OTP
                if not username:
                    messages.error(request, "Vui lòng nhập username.")
                    return render(request, 'login/forgot-password.html')
                elif not email:
                    messages.error(request, "Vui lòng nhập email.")
                    return render(request, 'login/forgot-password.html')
                elif not input_otp:
                    messages.error(request, "Vui lòng nhập OTP.")
                    return render(request, 'login/forgot-password.html')
                # Kiểm tra OTP đã tồn tại
                if username not in otp_storage:
                    messages.error(request, "OTP không tồn tại hoặc đã hết hạn.")
                    return render(request, 'login/forgot-password.html')
                stored_otp_data = otp_storage[username]
                stored_otp = stored_otp_data['otp']
                timestamp = stored_otp_data['timestamp']
                # Kiểm tra thời gian hiệu lực của OTP
                if time.time() - timestamp > 300:
                    del otp_storage[username]  # Xóa OTP đã hết hạn
                    messages.error(request, "OTP đã hết hạn. Vui lòng yêu cầu OTP mới.")
                    return render(request, 'login/forgot-password.html')
                # So khớp OTP
                if stored_otp != input_otp:
                    messages.error(request, "OTP không hợp lệ.")
                    return render(request, 'login/forgot-password.html')
                # Xóa OTP sau khi sử dụng
                del otp_storage[username]
                # Thực hiện logic đặt lại mật khẩu (hiển thị form đổi mật khẩu)
                messages.success(request, "Xác thực OTP thành công! Bạn có thể đặt lại mật khẩu.")
                return redirect('repassword_view', username=username)  # Redirect đến 're_password' với username

    except Exception as e:
        messages.error(f'error: {e}')
        return render(request, 'forgot_password.html')
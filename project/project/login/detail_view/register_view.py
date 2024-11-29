from django.shortcuts import render # tra ve 1 http response kem theo template html va du lieu cho nguoi dung
from django.shortcuts import redirect # dung de chuyen huong nguoi dung sang 1 url khac
from django.contrib import messages # tra va thong bao cho nguoi dung, nhung thong bao nay se hien owr template neu ban cau hinh
from django.contrib.auth import login # dung de dang nhap nguoi dung ngay sau khi tai khoan dc tao hoac xac thuc thanh cong
from django.contrib.auth.models import User # truong tac voi thong tin nguoi dung
from django.core.validators import validate_email # check xem 1 chuoi co phai la email hay khong
from django.core.exceptions import ValidationError # la 1 ngoai le(exception) dc sinh ra khi mot gia tri khong hop le theo yeu cau cua ung dung
import random # la 1 thu vien python de tao ra gia tri ngau nhien
import time # is a built- in python library for working with time
from common_service.otp import confirm
from django.contrib.messages import get_messages 

otp_storage = {}

def register_view(request):
    try:
        storage = get_messages(request)
        for _ in storage:
            pass  # Loại bỏ thông báo khỏi hàng đợi

        if request.method != 'POST':
            return render(request, 'login/register.html')
        else:
            '''get data form register form'''
            username = request.POST.get('username')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            input_otp = request.POST.get('otp')
            action = request.POST.get('action')

            '''check if fields are empty'''
            if not username or not email or not password1 or not password2:
                messages.error(request, "Vui lòng điền đầy đủ thông tin.")
                return render(request, 'login/register.html')

            # Kiểm tra mật khẩu có khớp không
            if password1 != password2:
                messages.error(request, "Mật khẩu không khớp. Vui lòng thử lại.")
                return render(request, 'login/register.html')

            # Kiểm tra xem tên người dùng đã tồn tại hay chưa
            if User.objects.filter(username=username).exists():
                messages.error(request, "Tên tài khoản đã tồn tại. Vui lòng chọn tên khác.")
                return render(request, 'login/register.html')

            # Kiểm tra xem email đã tồn tại hay chưa
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email đã tồn tại. Vui lòng sử dụng email khác.")
                return render(request, 'login/register.html')

            # Kiểm tra email có hợp lệ hay không
            try:
                validate_email(email)
            except ValidationError:
                messages.error(request, "Email không hợp lệ. Vui lòng nhập email đúng định dạng.")
                return render(request, 'login/register.html')

            if not input_otp:
                messages.error(request, "Vui lòng xác thực OTP. otp da dc gui den email cua ban")
                if username in otp_storage:
                    del otp_storage[username]
                otp = f'{random.randint(0, 9999):04}'  # create new otp
                otp_storage[username] = {'otp': otp, 'timestamp': time.time()}  # save otp with creation time
                '''send otp via email'''
                try:
                    title = 'Xác nhận thông tin'
                    content = f'Mã xác nhận của bạn là {otp}'
                    confirm(email, title, content)  # gọi hàm gửi email
                    # messages.success(request, 'OTP đã được gửi tới email của bạn. OTP chỉ có hiệu lực trong 5 phút.')
                except Exception as e:
                    messages.error(request, f'Không thể gửi email: {e}')
                return render(request, 'login/register.html')

            '''handle when action is "get_otp"'''
            if action == 'get_otp':
                '''delete old otp if it already exists'''
                if username in otp_storage:
                    del otp_storage[username]
                otp = f'{random.randint(0, 9999):04}'  # create new otp
                otp_storage[username] = {'otp': otp, 'timestamp': time.time()}  # save otp with creation time
                '''send otp via email'''
                try:
                    confirm(email, otp)  # gọi hàm gửi email
                    messages.success(request, 'OTP đã được gửi tới email của bạn. OTP chỉ có hiệu lực trong 5 phút.')
                except Exception as e:
                    messages.error(request, f'Không thể gửi email: {e}')
                return render(request, 'login/register.html')

            # Khi người dùng nhập OTP
            if action == 'confirm':
                '''check otp'''
                if username not in otp_storage:
                    messages.error(request, 'OTP không hợp lệ hoặc đã hết hạn. Vui lòng yêu cầu mã OTP mới.')
                    return render(request, 'login/register.html')

                stored_otp_data = otp_storage[username]
                stored_otp = stored_otp_data['otp']
                timestamp = stored_otp_data['timestamp']

                '''check otp validity period'''
                if time.time() - timestamp > 300:
                    del otp_storage[username]  # delete expired otp
                    messages.error(request, 'OTP đã hết hạn. Vui lòng yêu cầu mã OTP mới.')
                    return render(request, 'login/register.html')

                '''check otp'''
                if stored_otp != input_otp:
                    messages.error(request, 'OTP không chính xác.')
                    return render(request, 'login/register.html')
                else:
                    
                    try:
                        user = User.objects.create_user(
                            username=username,
                            email=email,
                            password=password1,
                            first_name=first_name,
                            last_name=last_name
                        )
                        user.save()  # Lưu dữ liệu vào MySQL
                        messages.success(request, 'Đăng ký thành công.')
                        return redirect('login')
                    except Exception as e:
                        messages.error(request, f'Lỗi: {e}')
                        return render(request, 'login/register.html')
    except Exception as e:
        print(f'Lỗi: {e}')
        messages.error(request, f'Lỗi: {e}')
        return render(request, 'login/register.html')
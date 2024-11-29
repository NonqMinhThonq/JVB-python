from django.shortcuts import render, redirect, get_object_or_404
from .models import University
from .forms import UniversityForm  # Form để chỉnh sửa thông tin trường
from common_service.otp import confirm
from django.utils import timezone  # Để lấy thời gian hiện tại

def manage_university(request):
    """
    View để quản lý thông tin trường học, thêm thông báo khi cập nhật thành công.
    """
    university = University.get_or_create_university(request.user)

    if request.method == 'POST':
        form = UniversityForm(request.POST, instance=university)
        if form.is_valid():
            form.save()  # Lưu thông tin cập nhật
            update_time = timezone.localtime(timezone.now()).strftime('%Y-%m-%d %H:%M')
            if 'notifications' not in request.session:
                request.session['notifications'] = []
            request.session['notifications'].insert(0,  # Thêm lên đầu danh sách
                f"University information updated successfully on {update_time}"
            )
            request.session.modified = True  
            try:
                user_email = request.user.email
                title = 'Notification'
                content = f'Your university information has been successfully updated on {update_time}!'
                confirm(receiver=user_email, title=title, content=content)
            except Exception as e:
                print(f"Error sending email: {e}")
            return redirect('manage_university')
    else:
        form = UniversityForm(instance=university)
    return render(
        request,
        'manage_university/university.html',
        {'form': form, 'university': university}
    )

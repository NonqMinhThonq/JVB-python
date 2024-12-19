from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..models import Student
from common_service.pagination import create_custom_page_range
from django.http import Http404
from django.utils import timezone
from common_service.otp import confirm
import datetime

@login_required
def student_list(request):
    search_query = request.GET.get('search', '').strip()
    if search_query:
        if search_query.isdigit():
            student_list = Student.objects.filter(
                created_by=request.user,
                id__icontains=search_query)
        else:
            student_list = Student.objects.filter(created_by=request.user)
            search_terms = search_query.split()
            for term in search_terms:
                # Sử dụng regex để chỉ tìm kiếm từ nguyên chính xác
                student_list = student_list.filter(name__iregex=rf'\b{term}\b')
    else:
        student_list = Student.objects.filter(created_by=request.user)

    paginator = Paginator(student_list, 10)
    page_number = request.GET.get('page')
    students = paginator.get_page(page_number)
    current_page = students.number
    total_pages = paginator.num_pages
    custom_page_range = create_custom_page_range(current_page, total_pages)
    return render(request, 'manage_student/student_list.html', {
        'students': students,
        'custom_page_range': custom_page_range,
        'search_query': search_query,
    })

@login_required
def student_delete(request, id):
    student = Student.objects.filter(id=id).first()
    if not student:
        raise Http404("Student not found")
    if request.method == 'POST':
        student_name = student.name
        student.delete() 
        if 'notifications' not in request.session:
            request.session['notifications'] = []
        notification_time = timezone.localtime(timezone.now()).strftime('%Y-%m-%d %H:%M')
        notification = f"The student '{student_name}' has been deleted on {notification_time}"
        request.session['notifications'].insert(0, notification)
        request.session.modified = True
        try:
            user_email = request.user.email
            title = 'Notification'
            content = f"The student '{student_name}' has been deleted on {notification_time}"
            confirm(receiver=user_email, title=title, content=content)
        except Exception as e:
            print(f"Error sending email: {e}")
        return redirect('student_list')
    return redirect('student_list')
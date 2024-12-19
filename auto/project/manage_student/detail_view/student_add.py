from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from ..models import Student, University, Major

def student_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        academic_year = request.POST.get('academic_year')
        university_id = request.POST.get('university')
        major_id = request.POST.get('major')
        quote = request.POST.get('quote', '')
        available = request.POST.get('available') == 'true'
        status = request.POST.get('status') == 'true'

        if not all([name, email, address, phone, academic_year, university_id]):
            messages.error(request, "All required fields must be filled.")
            return redirect('student_add')

        try:
            university = University.objects.get(id=university_id)
            major = Major.objects.get(id=major_id) if major_id else None
            new_student = Student(
                name=name,
                email=email,
                address=address,
                phone=phone,
                academic_year=academic_year,
                university=university,
                major=major,
                quote=quote,
                available=available,
                status=status,
                created_by=request.user
            )
            new_student.save()
            if 'notifications' not in request.session:
                request.session['notifications'] = []
            notification_time = timezone.localtime(timezone.now()).strftime('%Y-%m-%d %H:%M')
            notification = f"The student '{name}' dc tao luc {notification_time}"
            request.session['notifications'].insert(0, notification)
            request.session.modified = True
        except University.DoesNotExist:
            messages.error(request, "Selected university does not exist.")
        except Major.DoesNotExist:
            messages.error(request, "Selected major does not exist.")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
        return redirect('student_add')

    universities = University.objects.all()
    majors = Major.objects.all()

    return render(request, 'manage_student/student_add.html', {
        'universities': universities,
        'majors': majors
    })

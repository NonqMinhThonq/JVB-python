# student/models.py
from django.db import models
from manage_university.models import University  # Tham chiếu mô hình University từ app 'university'
from django.contrib.auth.models import User

class Major(models.Model):
    name = models.CharField(max_length=255)
    university = models.ForeignKey(University, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True)  # Đảm bảo email duy nhất
    address = models.TextField()
    phone = models.CharField(max_length=50)
    academic_year = models.CharField(max_length=50)
    university = models.ForeignKey(University, on_delete=models.CASCADE)  # Liên kết với University
    major = models.ForeignKey(Major, null=True, on_delete=models.SET_NULL)  # Liên kết với Major
    quote = models.CharField(max_length=255, blank=True, null=True)
    available = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='students') # Liên kết với User model

    def __str__(self):
        return self.email


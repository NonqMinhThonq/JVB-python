# models.py

from django.db import models
from django.contrib.auth.models import User

class University(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=50)
    current_academic_year = models.CharField(max_length=50, blank=True, null=True)
    year_of_establishment = models.CharField(max_length=50, blank=True, null=True)
    head_teacher = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    motto = models.CharField(max_length=255, blank=True, null=True)
    slogan = models.CharField(max_length=255, blank=True, null=True)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='universities')

    def __str__(self):
        return self.name

    @staticmethod
    def get_or_create_university(user):
        """Lấy hoặc tạo bản ghi duy nhất của trường cho người dùng"""
        university, created = University.objects.get_or_create(created_by=user)
        return university

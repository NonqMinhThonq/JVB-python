from django import forms
from .models import University

class UniversityForm(forms.ModelForm):
    class Meta:
        model = University
        fields = ['name', 'email', 'address', 'phone', 'current_academic_year', 'year_of_establishment', 'head_teacher', 'description', 'motto', 'slogan']

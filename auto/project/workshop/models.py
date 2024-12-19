from django.db import models
from django.contrib.auth.models import User
from manage_student.models import Major 

class Workshop(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    topic = models.ForeignKey(Major, null=True, on_delete=models.SET_NULL) 
    enterprise_id = models.IntegerField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workshop')

    def __str__(self):
        return f"{self.name} ({self.topic})"

from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserActivity(models.Model):
    page = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)  # Cambiar a DateField o DateTimeField
    departamento = models.CharField(max_length=100)


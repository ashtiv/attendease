from django.db import models
from django.contrib.auth.models import User


class checkTeacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_teacher = models.BooleanField(default=False)

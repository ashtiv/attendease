from django.db import models
from django.contrib.auth.models import User


class checkTeacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_teacher = models.BooleanField(default=False)


class Classes(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    password = models.CharField(max_length=100)
    teacher = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='classes')
    students = models.ManyToManyField(User, related_name='enrolled_classes')

    def __str__(self):
        return self.name

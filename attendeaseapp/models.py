from django.db import models
from django.contrib.auth.models import User


class checkTeacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_teacher = models.BooleanField(default=False)


class Classes(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    password = models.CharField(max_length=100)
    users = models.ManyToManyField(User, through='Enrollment')
    dates_present = models.JSONField(default=list)

    def __str__(self):
        return self.name


class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dates_present = models.JSONField(default=list)
    classes = models.ForeignKey(Classes, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}"


class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    classes = models.ForeignKey(Classes, on_delete=models.CASCADE)
    attendances = models.ManyToManyField(Attendance, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.classes.name}"

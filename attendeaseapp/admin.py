from django.contrib import admin

from .models import checkTeacher, Classes, Enrollment, Attendance

admin.site.register(checkTeacher)
admin.site.register(Classes)
admin.site.register(Enrollment)
admin.site.register(Attendance)

from django.contrib import admin
from django.urls import path
from attendeaseapp.views import register, login_view, logout_view, teacherhome, studenthome, index, search_classes, class_detail, attendance, add_attendance, remove_attendance, add_date, delete_date

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='home'),
    path('dashboard/teacher', teacherhome, name='teacherhome'),
    path('dashboard/student', studenthome, name='studenthome'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('search_classes/', search_classes, name='search_classes'),
    path('class/<int:class_id>/', class_detail, name='class_detail'),
    path('attendance/<int:class_id>/', attendance, name='attendance'),
    path('add_attendance/', add_attendance, name='add_attendance'),
    path('remove_attendance/', remove_attendance, name='remove_attendance'),
    path('add_date/', add_date, name='add_date'),
    path('delete_date/', delete_date, name='delete_date'),
]

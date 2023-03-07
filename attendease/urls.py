from django.contrib import admin
from django.urls import path
from attendeaseapp.views import register, login_view, logout_view, teacherhome, studenthome, index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='home'),
    path('dashboard/teacher', teacherhome, name='teacherhome'),
    path('dashboard/student', studenthome, name='studenthome'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]

from django.contrib import admin
from django.urls import path
from attendeaseapp.views import register, login_view, logout_view, teacherhome, studenthome, index, search_classes, class_detail

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
]

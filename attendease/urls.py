from django.contrib import admin
from django.urls import path
from attendeaseapp.views import register, login_view, logout_view, home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]

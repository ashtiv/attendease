from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from attendeaseapp.forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import checkTeacher, Classes, Enrollment
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.db.models import Q


def index(request):
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            is_teacher = request.POST.get('is_teacher', False)

            # Create a new checkTeacher instance for the user
            check_teacher = checkTeacher.objects.create(
                user=user, is_teacher=bool(is_teacher))

            messages.success(request, f'Account created for {username}!')

            # Automatically log in the user
            login(request, user)

            # Redirect to the appropriate home page based on the user's selection
            if is_teacher:
                return redirect('teacherhome')
            else:
                return redirect('studenthome')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if checkTeacher.objects.filter(user=user, is_teacher=True).exists():
                    # Redirect to teacher home
                    return redirect('teacherhome')
                else:
                    # Redirect to student home
                    return redirect('studenthome')
            else:
                messages.warning(request, 'Invalid username or password.')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required
def teacherhome(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            name = request.POST.get('class-name')
            description = request.POST.get('class-description')
            password = request.POST.get('class-password')

            # Create the class instance and catch any IntegrityError
            try:
                new_class = Classes.objects.create(
                    name=name, description=description, password=password)

                # Associate the current user with the new class
                Enrollment.objects.create(user=request.user, classes=new_class)

                # Success message
                messages.success(
                    request, f"The class '{name}' has been created.")
            except IntegrityError:
                # Error message
                messages.error(
                    request, f"A class with the name '{name}' already exists.")

        username = request.user.username

        # Get classes associated with current user
        teacher_classes = Classes.objects.filter(
            enrollment__user=request.user).values_list('name', 'description')

        # Get all classes
        all_classes = Classes.objects.all()

        return render(request, 'teacherhome.html', {'username': username, 'classes': teacher_classes, 'all_classes': all_classes})
    else:
        return redirect('login')


def studenthome(request):
    if request.user.is_authenticated:
        user = request.user
        user_classes = Enrollment.objects.filter(
            user=user).values_list('classes__name', flat=True)
        all_classes = Classes.objects.all()
        return render(request, 'studenthome.html', {'user_classes': user_classes, 'all_classes': all_classes})
    else:
        return redirect('login')


def search_classes(request):
    query = request.GET.get('query', '')
    if query:
        classes = Classes.objects.filter(Q(name__icontains=query))
    else:
        classes = Classes.objects.none()
    data = [{'name': c.name, 'description': c.description} for c in classes]
    return JsonResponse(data, safe=False)


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')

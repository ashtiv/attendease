from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from attendeaseapp.forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import checkTeacher, Classes, Enrollment, Attendance
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse
import qrcode
from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import base64


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
            enrollment__user=request.user).values_list('id', 'name', 'description')

        # Get all classes
        all_classes = Classes.objects.all()

        return render(request, 'teacherhome.html', {'username': username, 'classes': teacher_classes, 'all_classes': all_classes})
    else:
        return redirect('login')


@login_required(login_url='login')
def studenthome(request):
    user = request.user
    user_id = user.id
    qr_code = generate_qr_code(user_id)
    user_classes = Classes.objects.filter(
        enrollment__user=user).values_list('name', 'id', 'description')
    all_classes = Classes.objects.all()
    context = {'user_classes': user_classes,
               'all_classes': all_classes, 'qr_code': qr_code}
    return render(request, 'studenthome.html', context)


def generate_qr_code(user_id):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    value = f"student{user_id}student"
    qr.add_data(value)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer = buffer.getvalue()
    encoded_img = base64.b64encode(buffer).decode('utf-8')
    return encoded_img


@login_required
def search_classes(request):
    query = request.GET.get('query', '')
    if query:
        classes = Classes.objects.filter(Q(name__icontains=query))
    else:
        classes = Classes.objects.none()
    data = [{'name': c.name, 'description': c.description, 'id': c.id}
            for c in classes]
    return JsonResponse(data, safe=False)


@login_required
def class_detail(request, class_id):
    class_obj = get_object_or_404(Classes, id=class_id)
    enrolled = Enrollment.objects.filter(
        user=request.user, classes=class_obj).exists()
    if request.method == 'POST':
        password = request.POST.get('password')
        if password == class_obj.password:
            if not enrolled:
                Enrollment.objects.create(user=request.user, classes=class_obj)
                messages.success(
                    request, 'You have successfully joined the class.')
                # Replace 'success_page' with the name of your success page URL pattern
                # success_url = reverse('class_detail', args=[class_id])
                # return redirect(success_url)
            else:
                messages.warning(
                    request, 'You are already enrolled in this class.')
        else:
            messages.error(request, 'Incorrect password. Please try again.')
    enrollment = Enrollment.objects.filter(
        user=request.user, classes=class_obj).first()
    attendance_records = Attendance.objects.filter(
        user=request.user, classes=class_obj).first()
    dates_present = attendance_records.dates_present if attendance_records else []
    for attendance in dates_present:
        print(attendance)
    is_teacher = checkTeacher.objects.filter(
        user=request.user, is_teacher=True).exists()
    context = {'class_obj': class_obj, 'enrolled': enrolled,
               'attendance_records': dates_present, 'is_teacher': is_teacher}
    return render(request, 'class_detail.html', context)


def logout_view(request):
    logout(request)
    return redirect('home')

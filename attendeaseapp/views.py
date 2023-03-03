from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from attendeaseapp.forms import CustomUserCreationForm, CustomAuthenticationForm


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            # Authenticate the user and log them in.
            user = authenticate(request, username=user.username,
                                password=form.cleaned_data['password1'])
            login(request, user)
            return redirect('home')
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
                messages.success(request, f'Welcome back, {username}!')
                return redirect('home')
            else:
                messages.warning(request, 'Invalid username or password.')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})


def home(request):
    if request.user.is_authenticated:
        username = request.user.username
        return render(request, 'home.html', {'username': username})
    else:
        return redirect('login')


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')

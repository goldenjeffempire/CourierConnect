from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User
from .serializers import UserRegistrationSerializer


def register_view(request):
    if request.method == 'POST':
        serializer = UserRegistrationSerializer(data=request.POST)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('users:dashboard')
        else:
            for field, errors in serializer.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    
    return render(request, 'users/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            next_url = request.GET.get('next', 'users:dashboard')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'users/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('home')


@login_required
def dashboard_view(request):
    user = request.user
    
    if user.role == 'admin':
        return redirect('admin_panel:dashboard')
    elif user.role == 'courier':
        return redirect('courier:dashboard')
    else:
        return redirect('customer:dashboard')


@login_required
def profile_view(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.phone = request.POST.get('phone', user.phone)
        user.address = request.POST.get('address', user.address)
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('users:profile')
    
    return render(request, 'users/profile.html')

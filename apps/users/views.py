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


@login_required
def kyc_verification_view(request):
    user = request.user
    
    if request.method == 'POST':
        user.bvn = request.POST.get('bvn', '')
        user.nin = request.POST.get('nin', '')
        user.passport_number = request.POST.get('passport_number', '')
        user.drivers_license = request.POST.get('drivers_license', '')
        user.bank_name = request.POST.get('bank_name', '')
        user.account_number = request.POST.get('account_number', '')
        user.account_name = request.POST.get('account_name', '')
        user.date_of_birth = request.POST.get('date_of_birth') or None
        user.city = request.POST.get('city', '')
        user.state = request.POST.get('state', '')
        user.country = request.POST.get('country', '')
        user.postal_code = request.POST.get('postal_code', '')
        user.emergency_contact_name = request.POST.get('emergency_contact_name', '')
        user.emergency_contact_phone = request.POST.get('emergency_contact_phone', '')
        user.emergency_contact_relationship = request.POST.get('emergency_contact_relationship', '')
        
        if 'id_card_front' in request.FILES:
            user.id_card_front = request.FILES['id_card_front']
        if 'id_card_back' in request.FILES:
            user.id_card_back = request.FILES['id_card_back']
        if 'utility_bill' in request.FILES:
            user.utility_bill = request.FILES['utility_bill']
        if 'profile_photo' in request.FILES:
            user.profile_photo = request.FILES['profile_photo']
        
        user.kyc_submitted = True
        from django.utils import timezone
        user.kyc_submission_date = timezone.now()
        user.save()
        
        messages.success(request, 'KYC information submitted successfully! Your verification is being processed.')
        return redirect('users:profile')
    
    return render(request, 'users/kyc_verification.html', {'user': user})

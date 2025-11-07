from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from decimal import Decimal
from geopy.distance import geodesic
import random
import string
from .models import Parcel
from apps.tracking.models import TrackingEvent


def generate_tracking_number():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))


def calculate_rate(weight, distance, service_type='standard'):
    base_rate = Decimal('5.00')
    weight_rate = Decimal(str(weight)) * Decimal('0.50')
    distance_rate = Decimal(str(distance)) * Decimal('0.10')
    
    total = base_rate + weight_rate + distance_rate
    
    if service_type == 'express':
        total = total * Decimal('1.5')
    
    return round(total, 2)


@login_required
def create_parcel_view(request):
    if request.method == 'POST':
        tracking_number = generate_tracking_number()
        
        pickup_lat = request.POST.get('pickup_lat', 40.7128)
        pickup_lng = request.POST.get('pickup_lng', -74.0060)
        dropoff_lat = request.POST.get('dropoff_lat', 34.0522)
        dropoff_lng = request.POST.get('dropoff_lng', -118.2437)
        
        distance = geodesic(
            (float(pickup_lat), float(pickup_lng)),
            (float(dropoff_lat), float(dropoff_lng))
        ).miles
        
        weight = Decimal(request.POST.get('weight', 5))
        service_type = request.POST.get('service_type', 'standard')
        
        price = calculate_rate(weight, distance, service_type)
        
        parcel = Parcel.objects.create(
            tracking_number=tracking_number,
            customer=request.user,
            pickup_address=request.POST.get('pickup_address'),
            pickup_lat=pickup_lat,
            pickup_lng=pickup_lng,
            dropoff_address=request.POST.get('dropoff_address'),
            dropoff_lat=dropoff_lat,
            dropoff_lng=dropoff_lng,
            package_description=request.POST.get('package_description', ''),
            weight=weight,
            length=request.POST.get('length'),
            width=request.POST.get('width'),
            height=request.POST.get('height'),
            service_type=service_type,
            price=price
        )
        
        TrackingEvent.objects.create(
            parcel=parcel,
            status='pending',
            description='Parcel created and awaiting payment'
        )
        
        messages.success(request, f'Parcel created! Tracking number: {tracking_number}')
        return redirect('parcels:payment', tracking_number=tracking_number)
    
    return render(request, 'parcels/create.html')


def get_quote_view(request):
    if request.method == 'POST':
        weight = float(request.POST.get('weight', 5))
        distance = float(request.POST.get('distance', 100))
        service_type = request.POST.get('service_type', 'standard')
        
        price = calculate_rate(weight, distance, service_type)
        
        return JsonResponse({
            'price': str(price),
            'currency': 'USD',
            'estimated_delivery': '3-5 business days' if service_type == 'standard' else '1-2 business days'
        })
    
    return render(request, 'parcels/quote.html')


def parcel_detail_view(request, tracking_number):
    parcel = get_object_or_404(Parcel, tracking_number=tracking_number)
    tracking_events = parcel.tracking_events.all()
    
    context = {
        'parcel': parcel,
        'tracking_events': tracking_events
    }
    return render(request, 'parcels/detail.html', context)


@login_required
def payment_view(request, tracking_number):
    parcel = get_object_or_404(Parcel, tracking_number=tracking_number, customer=request.user)
    
    context = {
        'parcel': parcel,
        'stripe_publishable_key': 'pk_test_DEMO_PUBLISHABLE'
    }
    return render(request, 'parcels/payment.html', context)

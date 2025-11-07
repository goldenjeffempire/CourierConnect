#!/usr/bin/env python
import os
import django
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'courier.settings.dev')
django.setup()

from django.contrib.auth import get_user_model
from apps.parcels.models import Parcel
from apps.tracking.models import TrackingEvent
from decimal import Decimal
import random
from datetime import timedelta
from django.utils import timezone

User = get_user_model()

def generate_tracking_number():
    import string
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))

def create_users():
    print("Creating users...")
    
    admin = User.objects.create_superuser(
        username='admin',
        email='admin@couriercore.com',
        password='admin123',
        first_name='Admin',
        last_name='User',
        role='admin'
    )
    
    customers = []
    for i in range(1, 11):
        customer = User.objects.create_user(
            username=f'customer{i}',
            email=f'customer{i}@example.com',
            password='password123',
            first_name=f'Customer',
            last_name=f'{i}',
            role='customer',
            phone=f'+1-555-{1000+i:04d}'
        )
        customers.append(customer)
    
    couriers = []
    for i in range(1, 6):
        courier = User.objects.create_user(
            username=f'courier{i}',
            email=f'courier{i}@example.com',
            password='password123',
            first_name=f'Driver',
            last_name=f'{i}',
            role='courier',
            phone=f'+1-555-{2000+i:04d}'
        )
        couriers.append(courier)
    
    print(f"Created 1 admin, {len(customers)} customers, {len(couriers)} couriers")
    return admin, customers, couriers

def create_parcels(customers, couriers):
    print("Creating parcels...")
    
    addresses = [
        ("123 Main St, New York, NY 10001", 40.7128, -74.0060),
        ("456 Market St, San Francisco, CA 94102", 37.7749, -122.4194),
        ("789 Lake Shore Dr, Chicago, IL 60611", 41.8781, -87.6298),
        ("321 Peachtree St, Atlanta, GA 30303", 33.7490, -84.3880),
        ("654 Congress Ave, Austin, TX 78701", 30.2672, -97.7431),
        ("987 Broadway, Seattle, WA 98122", 47.6062, -122.3321),
        ("147 Ocean Dr, Miami, FL 33139", 25.7617, -80.1918),
        ("258 Boylston St, Boston, MA 02116", 42.3601, -71.0589),
        ("369 Pennsylvania Ave, Washington, DC 20004", 38.9072, -77.0369),
        ("741 Fremont St, Las Vegas, NV 89101", 36.1699, -115.1398),
    ]
    
    statuses = ['pending', 'assigned', 'picked_up', 'in_transit', 'out_for_delivery', 'delivered']
    service_types = ['standard', 'express']
    
    parcels = []
    for i in range(20):
        pickup = random.choice(addresses)
        dropoff = random.choice([a for a in addresses if a != pickup])
        
        customer = random.choice(customers)
        courier = random.choice(couriers) if i % 2 == 0 else None
        
        service_type = random.choice(service_types)
        weight = Decimal(str(random.uniform(1, 50)))
        price = Decimal('5.00') + weight * Decimal('0.50') + Decimal(str(random.uniform(10, 100)))
        
        if service_type == 'express':
            price = price * Decimal('1.5')
        
        parcel = Parcel.objects.create(
            tracking_number=generate_tracking_number(),
            customer=customer,
            courier=courier,
            pickup_address=pickup[0],
            pickup_lat=pickup[1],
            pickup_lng=pickup[2],
            dropoff_address=dropoff[0],
            dropoff_lat=dropoff[1],
            dropoff_lng=dropoff[2],
            package_description=f"Package #{i+1} - {random.choice(['Documents', 'Electronics', 'Clothing', 'Books', 'Gifts'])}",
            weight=weight,
            service_type=service_type,
            status=random.choice(statuses),
            price=round(price, 2),
            paid=random.choice([True, False]),
            created_at=timezone.now() - timedelta(days=random.randint(0, 30))
        )
        parcels.append(parcel)
        
        num_events = random.randint(1, 5)
        for j in range(num_events):
            TrackingEvent.objects.create(
                parcel=parcel,
                status=random.choice(statuses),
                description=f"Event #{j+1}: {random.choice(['Package scanned', 'In transit', 'Out for delivery', 'Delivered'])}",
                location=random.choice([a[0] for a in addresses]),
                latitude=random.choice([a[1] for a in addresses]),
                longitude=random.choice([a[2] for a in addresses]),
                timestamp=parcel.created_at + timedelta(hours=j*6)
            )
    
    print(f"Created {len(parcels)} parcels with tracking events")
    return parcels

def main():
    print("Starting seed data generation...")
    
    print("Clearing existing data...")
    TrackingEvent.objects.all().delete()
    Parcel.objects.all().delete()
    User.objects.all().delete()
    
    admin, customers, couriers = create_users()
    parcels = create_parcels(customers, couriers)
    
    print("\n" + "="*50)
    print("Demo data created successfully!")
    print("="*50)
    print("\nTest accounts:")
    print("Admin: username=admin, password=admin123")
    print("Customer: username=customer1, password=password123")
    print("Courier: username=courier1, password=password123")
    print("\nTotal records:")
    print(f"- Users: {User.objects.count()}")
    print(f"- Parcels: {Parcel.objects.count()}")
    print(f"- Tracking Events: {TrackingEvent.objects.count()}")
    print("="*50)

if __name__ == '__main__':
    main()

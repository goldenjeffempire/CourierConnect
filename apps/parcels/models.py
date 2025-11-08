from django.db import models
from django.conf import settings
from django.utils import timezone
import random
import string


def generate_tracking_number():
    prefix = "GC"
    numbers = ''.join(random.choices(string.digits, k=10))
    return f"{prefix}{numbers}"


def generate_delivery_code():
    return ''.join(random.choices(string.digits, k=6))


class Parcel(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('assigned', 'Assigned to Courier'),
        ('picked_up', 'Picked Up'),
        ('in_transit', 'In Transit'),
        ('held_at_customs', 'Held at Customs'),
        ('awaiting_clearance', 'Awaiting Clearance'),
        ('payment_required', 'Payment Required'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('failed_delivery', 'Failed Delivery Attempt'),
        ('return_to_sender', 'Return to Sender'),
        ('cancelled', 'Cancelled'),
    ]
    
    SERVICE_CHOICES = [
        ('standard', 'Standard Shipping'),
        ('express', 'Express Shipping'),
        ('overnight', 'Overnight Delivery'),
    ]
    
    tracking_number = models.CharField(max_length=20, unique=True, default=generate_tracking_number)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='parcels')
    courier = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_parcels')
    
    sender_name = models.CharField(max_length=255, default='')
    sender_phone = models.CharField(max_length=20, default='')
    sender_email = models.EmailField(blank=True, default='')
    sender_address = models.TextField(default='')
    
    receiver_name = models.CharField(max_length=255, default='')
    receiver_phone = models.CharField(max_length=20, default='')
    receiver_email = models.EmailField(blank=True, default='')
    receiver_address = models.TextField(default='')
    
    pickup_address = models.TextField()
    pickup_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    pickup_lng = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    dropoff_address = models.TextField()
    dropoff_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    dropoff_lng = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    package_description = models.TextField()
    package_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    length = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    width = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    height = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    parcel_photo = models.ImageField(upload_to='parcels/photos/', null=True, blank=True)
    
    service_type = models.CharField(max_length=20, choices=SERVICE_CHOICES, default='standard')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='pending')
    
    delivery_code = models.CharField(max_length=6, default=generate_delivery_code)
    delivery_code_verified = models.BooleanField(default=False)
    
    driver_name = models.CharField(max_length=255, blank=True)
    driver_phone = models.CharField(max_length=20, blank=True)
    driver_photo = models.ImageField(upload_to='drivers/photos/', null=True, blank=True)
    
    estimated_delivery = models.DateTimeField(null=True, blank=True)
    pickup_time = models.DateTimeField(null=True, blank=True)
    delivery_time = models.DateTimeField(null=True, blank=True)
    deadline = models.DateTimeField(null=True, blank=True, help_text="Deadline before parcel returns to sender")
    
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    customs_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    clearance_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    paid = models.BooleanField(default=False)
    customs_paid = models.BooleanField(default=False)
    clearance_paid = models.BooleanField(default=False)
    delivery_paid = models.BooleanField(default=False)
    
    kyc_verified = models.BooleanField(default=False)
    kyc_required = models.BooleanField(default=False)
    
    urgent = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'parcels'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['tracking_number']),
            models.Index(fields=['status']),
            models.Index(fields=['customer']),
            models.Index(fields=['delivery_code']),
        ]
        
    def __str__(self):
        return f"Parcel {self.tracking_number}"
    
    def get_total_amount(self):
        return self.price + self.customs_fee + self.clearance_fee + self.delivery_fee
    
    def is_deadline_approaching(self):
        if self.deadline:
            time_remaining = self.deadline - timezone.now()
            return time_remaining.total_seconds() < 86400
        return False
    
    def get_time_remaining(self):
        if self.deadline:
            time_remaining = self.deadline - timezone.now()
            if time_remaining.total_seconds() > 0:
                hours = int(time_remaining.total_seconds() // 3600)
                minutes = int((time_remaining.total_seconds() % 3600) // 60)
                return f"{hours}h {minutes}m"
            return "Expired"
        return None

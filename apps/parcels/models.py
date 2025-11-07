from django.db import models
from django.conf import settings


class Parcel(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('assigned', 'Assigned to Courier'),
        ('picked_up', 'Picked Up'),
        ('in_transit', 'In Transit'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    SERVICE_CHOICES = [
        ('standard', 'Standard'),
        ('express', 'Express'),
    ]
    
    tracking_number = models.CharField(max_length=20, unique=True)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='parcels')
    courier = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_parcels')
    
    pickup_address = models.TextField()
    pickup_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    pickup_lng = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    dropoff_address = models.TextField()
    dropoff_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    dropoff_lng = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    package_description = models.TextField()
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    length = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    width = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    height = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    service_type = models.CharField(max_length=20, choices=SERVICE_CHOICES, default='standard')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    estimated_delivery = models.DateTimeField(null=True, blank=True)
    pickup_time = models.DateTimeField(null=True, blank=True)
    delivery_time = models.DateTimeField(null=True, blank=True)
    
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    paid = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'parcels'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['tracking_number']),
            models.Index(fields=['status']),
            models.Index(fields=['customer']),
        ]
        
    def __str__(self):
        return f"Parcel {self.tracking_number}"

from django.db import models
from django.conf import settings
from apps.parcels.models import Parcel


class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    PROVIDER_CHOICES = [
        ('stripe', 'Stripe'),
        ('paystack', 'Paystack'),
    ]
    
    parcel = models.ForeignKey(Parcel, on_delete=models.CASCADE, related_name='payments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    provider = models.CharField(max_length=20, choices=PROVIDER_CHOICES, default='stripe')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    transaction_id = models.CharField(max_length=255, blank=True)
    payment_intent_id = models.CharField(max_length=255, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'payments'
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Payment {self.id} - {self.amount} {self.currency}"

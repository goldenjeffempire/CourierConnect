from django.db import models
from django.conf import settings
from apps.parcels.models import Parcel
import uuid


class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
        ('under_review', 'Under Review'),
    ]
    
    PROVIDER_CHOICES = [
        ('stripe', 'Stripe'),
        ('paystack', 'Paystack'),
        ('bank_transfer', 'Bank Transfer'),
        ('cash', 'Cash'),
    ]
    
    PAYMENT_TYPE_CHOICES = [
        ('shipping', 'Shipping Fee'),
        ('customs', 'Customs Fee'),
        ('clearance', 'Clearance Fee'),
        ('delivery', 'Delivery Fee'),
        ('insurance', 'Insurance Fee'),
        ('storage', 'Storage Fee'),
    ]
    
    parcel = models.ForeignKey(Parcel, on_delete=models.CASCADE, related_name='payments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    provider = models.CharField(max_length=20, choices=PROVIDER_CHOICES, default='stripe')
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES, default='shipping')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    transaction_id = models.CharField(max_length=255, blank=True)
    payment_intent_id = models.CharField(max_length=255, blank=True)
    invoice_number = models.CharField(max_length=50, unique=True, blank=True)
    receipt_number = models.CharField(max_length=50, unique=True, blank=True)
    
    proof_of_payment = models.ImageField(upload_to='payments/proofs/', null=True, blank=True)
    payment_screenshot = models.ImageField(upload_to='payments/screenshots/', null=True, blank=True)
    
    confirmation_sent = models.BooleanField(default=False)
    thank_you_sent = models.BooleanField(default=False)
    
    notes = models.TextField(blank=True)
    admin_notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'payments'
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Payment {self.id} - {self.amount} {self.currency}"
    
    def save(self, *args, **kwargs):
        if not self.invoice_number:
            self.invoice_number = f"INV-{uuid.uuid4().hex[:10].upper()}"
        if not self.receipt_number:
            self.receipt_number = f"RCT-{uuid.uuid4().hex[:10].upper()}"
        super().save(*args, **kwargs)
    
    def get_payment_type_display_full(self):
        return dict(self.PAYMENT_TYPE_CHOICES).get(self.payment_type, self.payment_type)

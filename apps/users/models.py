from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('courier', 'Courier'),
        ('admin', 'Admin'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    
    profile_photo = models.ImageField(upload_to='users/photos/', null=True, blank=True)
    
    bvn = models.CharField(max_length=20, blank=True, verbose_name="Bank Verification Number")
    nin = models.CharField(max_length=20, blank=True, verbose_name="National Identification Number")
    passport_number = models.CharField(max_length=50, blank=True)
    drivers_license = models.CharField(max_length=50, blank=True)
    
    id_card_front = models.ImageField(upload_to='users/kyc/id_front/', null=True, blank=True)
    id_card_back = models.ImageField(upload_to='users/kyc/id_back/', null=True, blank=True)
    utility_bill = models.ImageField(upload_to='users/kyc/utility/', null=True, blank=True)
    
    bank_name = models.CharField(max_length=100, blank=True)
    account_number = models.CharField(max_length=20, blank=True)
    account_name = models.CharField(max_length=255, blank=True)
    
    kyc_verified = models.BooleanField(default=False)
    kyc_submitted = models.BooleanField(default=False)
    kyc_submission_date = models.DateTimeField(null=True, blank=True)
    kyc_verification_date = models.DateTimeField(null=True, blank=True)
    kyc_notes = models.TextField(blank=True)
    
    emergency_contact_name = models.CharField(max_length=255, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    emergency_contact_relationship = models.CharField(max_length=100, blank=True)
    
    date_of_birth = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'users'
        
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    def get_full_name_or_username(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username

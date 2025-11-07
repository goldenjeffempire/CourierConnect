from django.db import models
from apps.parcels.models import Parcel


class TrackingEvent(models.Model):
    parcel = models.ForeignKey(Parcel, on_delete=models.CASCADE, related_name='tracking_events')
    status = models.CharField(max_length=50)
    description = models.TextField()
    location = models.CharField(max_length=255, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'tracking_events'
        ordering = ['-timestamp']
        
    def __str__(self):
        return f"{self.parcel.tracking_number} - {self.status}"

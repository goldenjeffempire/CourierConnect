
from celery import shared_task
from django.contrib.auth import get_user_model
from .email_service import EmailNotificationService
from .sms_service import SMSNotificationService

User = get_user_model()


@shared_task
def send_shipment_confirmation_email(parcel_id, user_id):
    """Send shipment confirmation email asynchronously"""
    from apps.parcels.models import Parcel
    
    try:
        parcel = Parcel.objects.get(id=parcel_id)
        user = User.objects.get(id=user_id)
        
        EmailNotificationService.send_shipment_confirmation(parcel, user)
        return f"Shipment confirmation sent for {parcel.tracking_number}"
    except Exception as e:
        return f"Error sending shipment confirmation: {str(e)}"


@shared_task
def send_payment_confirmation_email(parcel_id, payment_id):
    """Send payment confirmation email asynchronously"""
    from apps.parcels.models import Parcel
    from apps.payments.models import Payment
    
    try:
        parcel = Parcel.objects.get(id=parcel_id)
        payment = Payment.objects.get(id=payment_id)
        
        EmailNotificationService.send_payment_confirmation(parcel, payment)
        return f"Payment confirmation sent for {parcel.tracking_number}"
    except Exception as e:
        return f"Error sending payment confirmation: {str(e)}"


@shared_task
def send_status_update_email(parcel_id, status, description):
    """Send status update email asynchronously"""
    from apps.parcels.models import Parcel
    
    try:
        parcel = Parcel.objects.get(id=parcel_id)
        
        EmailNotificationService.send_status_update(parcel, status, description)
        return f"Status update sent for {parcel.tracking_number}"
    except Exception as e:
        return f"Error sending status update: {str(e)}"


@shared_task
def send_delivery_confirmation_email(parcel_id):
    """Send delivery confirmation email asynchronously"""
    from apps.parcels.models import Parcel
    
    try:
        parcel = Parcel.objects.get(id=parcel_id)
        
        EmailNotificationService.send_delivery_confirmation(parcel)
        return f"Delivery confirmation sent for {parcel.tracking_number}"
    except Exception as e:
        return f"Error sending delivery confirmation: {str(e)}"


@shared_task
def send_sms_notification(phone_number, message):
    """Send SMS notification asynchronously"""
    try:
        SMSNotificationService.send_sms(phone_number, message)
        return f"SMS sent to {phone_number}"
    except Exception as e:
        return f"Error sending SMS: {str(e)}"

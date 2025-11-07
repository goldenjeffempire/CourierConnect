
from django.conf import settings
from twilio.rest import Client


class SMSNotificationService:
    """
    SMS notification service using Twilio
    """
    
    @staticmethod
    def send_sms(phone_number, message):
        """Send SMS notification"""
        if not hasattr(settings, 'TWILIO_ACCOUNT_SID') or settings.TWILIO_ACCOUNT_SID == 'ACDEMO':
            # Demo mode - just log the message
            print(f"[SMS Demo] To: {phone_number}, Message: {message}")
            return True
        
        try:
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            
            message = client.messages.create(
                body=message,
                from_=settings.TWILIO_PHONE_NUMBER,
                to=phone_number
            )
            
            return message.sid
        except Exception as e:
            print(f"Error sending SMS: {str(e)}")
            return False
    
    @staticmethod
    def send_tracking_update(parcel, status):
        """Send tracking update via SMS"""
        message = f"Courier Core: Your package {parcel.tracking_number} is now {status}. Track at: couriercore.com/tracking/{parcel.tracking_number}"
        
        if parcel.customer.phone:
            return SMSNotificationService.send_sms(parcel.customer.phone, message)
        
        return False
    
    @staticmethod
    def send_delivery_otp(parcel, otp):
        """Send delivery OTP via SMS"""
        message = f"Courier Core: Your delivery OTP is {otp}. Share this with the courier to confirm delivery of {parcel.tracking_number}"
        
        if parcel.customer.phone:
            return SMSNotificationService.send_sms(parcel.customer.phone, message)
        
        return False

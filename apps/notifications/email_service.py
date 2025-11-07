
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags


class EmailNotificationService:
    """
    Comprehensive email notification service for courier operations
    """
    
    @staticmethod
    def send_shipment_confirmation(parcel, user):
        """Send shipment creation confirmation"""
        subject = f'Shipment Created - {parcel.tracking_number}'
        
        context = {
            'user': user,
            'parcel': parcel,
            'tracking_url': f'{settings.SITE_URL}/tracking/{parcel.tracking_number}/'
        }
        
        html_message = render_to_string('emails/shipment_confirmation.html', context)
        plain_message = strip_tags(html_message)
        
        return send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False
        )
    
    @staticmethod
    def send_payment_confirmation(parcel, payment):
        """Send payment confirmation"""
        subject = f'Payment Confirmed - {parcel.tracking_number}'
        
        context = {
            'parcel': parcel,
            'payment': payment,
            'tracking_url': f'{settings.SITE_URL}/tracking/{parcel.tracking_number}/'
        }
        
        html_message = render_to_string('emails/payment_confirmation.html', context)
        plain_message = strip_tags(html_message)
        
        return send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[parcel.customer.email],
            html_message=html_message,
            fail_silently=False
        )
    
    @staticmethod
    def send_status_update(parcel, status, description):
        """Send shipment status update"""
        subject = f'Shipment Update - {parcel.tracking_number}'
        
        context = {
            'parcel': parcel,
            'status': status,
            'description': description,
            'tracking_url': f'{settings.SITE_URL}/tracking/{parcel.tracking_number}/'
        }
        
        html_message = render_to_string('emails/status_update.html', context)
        plain_message = strip_tags(html_message)
        
        return send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[parcel.customer.email],
            html_message=html_message,
            fail_silently=False
        )
    
    @staticmethod
    def send_delivery_confirmation(parcel):
        """Send delivery confirmation with OTP"""
        subject = f'Delivered - {parcel.tracking_number}'
        
        context = {
            'parcel': parcel,
            'customer': parcel.customer
        }
        
        html_message = render_to_string('emails/delivery_confirmation.html', context)
        plain_message = strip_tags(html_message)
        
        return send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[parcel.customer.email],
            html_message=html_message,
            fail_silently=False
        )

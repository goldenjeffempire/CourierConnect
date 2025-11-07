from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from apps.parcels.models import Parcel
from apps.tracking.models import TrackingEvent
from .models import Payment
import json


@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    
    try:
        event_data = json.loads(payload)
        event_type = event_data.get('type')
        
        if event_type == 'payment_intent.succeeded':
            payment_intent = event_data.get('data', {}).get('object', {})
            payment_intent_id = payment_intent.get('id')
            
            try:
                payment = Payment.objects.get(payment_intent_id=payment_intent_id)
                payment.status = 'completed'
                payment.transaction_id = payment_intent.get('charges', {}).get('data', [{}])[0].get('id', '')
                payment.save()
                
                parcel = payment.parcel
                parcel.paid = True
                parcel.status = 'assigned'
                parcel.save()
                
                TrackingEvent.objects.create(
                    parcel=parcel,
                    status='assigned',
                    description='Payment received. Parcel is being assigned to a courier.'
                )
                
                # Send payment confirmation email
                from apps.notifications.tasks import send_payment_confirmation_email, send_status_update_email
                send_payment_confirmation_email.delay(parcel.id, payment.id)
                send_status_update_email.delay(parcel.id, 'assigned', 'Payment received. Your shipment will be assigned to a courier shortly.')
            except Payment.DoesNotExist:
                pass
        
        return HttpResponse(status=200)
    except Exception as e:
        return HttpResponse(status=400)


@login_required
def payment_success_view(request):
    tracking_number = request.GET.get('tracking_number')
    
    if tracking_number:
        parcel = get_object_or_404(Parcel, tracking_number=tracking_number)
        context = {'parcel': parcel}
        return render(request, 'payments/success.html', context)
    
    return redirect('home')


@login_required
def payment_cancel_view(request):
    messages.warning(request, 'Payment was cancelled')
    return render(request, 'payments/cancel.html')

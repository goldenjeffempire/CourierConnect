from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from apps.parcels.models import Parcel
from apps.tracking.models import TrackingEvent
from .models import Payment
from .utils import generate_invoice_pdf, generate_receipt_pdf
import json


def can_access_parcel(user, parcel):
    """Check if user has permission to access parcel payment data."""
    if user.role == 'admin':
        return True
    if parcel.customer == user:
        return True
    if parcel.courier and parcel.courier == user:
        return True
    return False


def can_access_payment(user, payment):
    """Check if user has permission to access payment data."""
    if user.role == 'admin':
        return True
    if payment.user == user:
        return True
    if payment.parcel.customer == user:
        return True
    if payment.parcel.courier and payment.parcel.courier == user:
        return True
    return False


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
                
            except Payment.DoesNotExist:
                pass
        
        return HttpResponse(status=200)
    except Exception as e:
        return HttpResponse(status=400)


@login_required
def payment_page_view(request, parcel_id):
    parcel = get_object_or_404(Parcel, id=parcel_id)
    
    if not can_access_parcel(request.user, parcel):
        return HttpResponse('Unauthorized: You do not have permission to access this parcel.', status=403)
    
    pending_fees = []
    if not parcel.paid:
        pending_fees.append({'type': 'shipping', 'amount': parcel.price, 'name': 'Shipping Fee'})
    if not parcel.customs_paid and parcel.customs_fee > 0:
        pending_fees.append({'type': 'customs', 'amount': parcel.customs_fee, 'name': 'Customs Fee'})
    if not parcel.clearance_paid and parcel.clearance_fee > 0:
        pending_fees.append({'type': 'clearance', 'amount': parcel.clearance_fee, 'name': 'Clearance Fee'})
    if not parcel.delivery_paid and parcel.delivery_fee > 0:
        pending_fees.append({'type': 'delivery', 'amount': parcel.delivery_fee, 'name': 'Delivery Fee'})
    
    context = {
        'parcel': parcel,
        'pending_fees': pending_fees,
        'total_pending': sum(fee['amount'] for fee in pending_fees),
        'stripe_publishable_key': 'pk_test_DEMO_PUBLISHABLE'
    }
    return render(request, 'parcels/payment.html', context)


@login_required
def upload_proof_of_payment_view(request, parcel_id):
    if request.method == 'POST':
        parcel = get_object_or_404(Parcel, id=parcel_id)
        
        if not can_access_parcel(request.user, parcel):
            return HttpResponse('Unauthorized: You do not have permission to upload proof of payment for this parcel.', status=403)
        
        payment_type = request.POST.get('payment_type', 'shipping')
        proof_file = request.FILES.get('proof_of_payment')
        
        if proof_file:
            amount_map = {
                'shipping': parcel.price,
                'customs': parcel.customs_fee,
                'clearance': parcel.clearance_fee,
                'delivery': parcel.delivery_fee,
            }
            
            payment = Payment.objects.create(
                parcel=parcel,
                user=request.user,
                provider='bank_transfer',
                payment_type=payment_type,
                amount=amount_map.get(payment_type, 0),
                currency='USD',
                status='under_review',
                proof_of_payment=proof_file,
            )
            
            messages.success(request, 'Payment proof uploaded successfully. Awaiting verification.')
            return redirect('payment_page', parcel_id=parcel.id)
    
    return redirect('payment_page', parcel_id=parcel_id)


@login_required
def download_invoice_view(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    
    if not can_access_payment(request.user, payment):
        return HttpResponse('Unauthorized: You do not have permission to access this invoice.', status=403)
    
    pdf_buffer = generate_invoice_pdf(payment)
    
    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{payment.invoice_number}.pdf"'
    return response


@login_required
def download_receipt_view(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    
    if not can_access_payment(request.user, payment):
        return HttpResponse('Unauthorized: You do not have permission to access this receipt.', status=403)
    
    pdf_buffer = generate_receipt_pdf(payment)
    
    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="receipt_{payment.receipt_number}.pdf"'
    return response


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

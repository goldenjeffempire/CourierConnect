from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from apps.parcels.models import Parcel
from .models import TrackingEvent


def track_parcel_view(request, tracking_number=None):
    parcel = None
    tracking_events = []
    progress_percentage = 0
    timeline_steps = []
    
    if request.method == 'POST' or tracking_number:
        tracking_num = tracking_number or request.POST.get('tracking_number', '').strip()
        
        try:
            parcel = Parcel.objects.get(tracking_number=tracking_num)
            tracking_events = parcel.tracking_events.all().order_by('-timestamp')
            
            status_map = {
                'pending': 10,
                'assigned': 20,
                'picked_up': 35,
                'in_transit': 50,
                'held_at_customs': 60,
                'awaiting_clearance': 65,
                'payment_required': 70,
                'out_for_delivery': 85,
                'delivered': 100,
            }
            progress_percentage = status_map.get(parcel.status, 50)
            
            timeline_steps = [
                {'name': 'Order Placed', 'status': 'pending', 'completed': parcel.status != 'pending'},
                {'name': 'In Transit', 'status': 'in_transit', 'completed': parcel.status in ['in_transit', 'held_at_customs', 'awaiting_clearance', 'payment_required', 'out_for_delivery', 'delivered']},
                {'name': 'Customs Processing', 'status': 'held_at_customs', 'completed': parcel.status in ['awaiting_clearance', 'payment_required', 'out_for_delivery', 'delivered']},
                {'name': 'Out for Delivery', 'status': 'out_for_delivery', 'completed': parcel.status in ['out_for_delivery', 'delivered']},
                {'name': 'Delivered', 'status': 'delivered', 'completed': parcel.status == 'delivered'},
            ]
            
        except Parcel.DoesNotExist:
            parcel = None
    
    context = {
        'parcel': parcel,
        'tracking_events': tracking_events,
        'progress_percentage': progress_percentage,
        'timeline_steps': timeline_steps,
        'mapbox_token': 'pk.mapbox_demo_token_12345',
        'tracking_number_searched': tracking_number,
    }
    return render(request, 'tracking/track.html', context)


@login_required
def update_status_view(request, parcel_id):
    if request.method == 'POST':
        parcel = get_object_or_404(Parcel, id=parcel_id)
        
        if request.user.role not in ['admin', 'courier']:
            return JsonResponse({'success': False, 'message': 'Unauthorized'}, status=403)
        
        new_status = request.POST.get('status')
        description = request.POST.get('description', f'Status updated to {new_status}')
        location = request.POST.get('location', '')
        
        if new_status:
            parcel.status = new_status
            parcel.save()
            
            TrackingEvent.objects.create(
                parcel=parcel,
                status=new_status,
                description=description,
                location=location,
                timestamp=timezone.now()
            )
            
            return JsonResponse({'success': True, 'message': 'Status updated successfully'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)


@login_required
@csrf_exempt
def update_location_view(request, parcel_id):
    if request.method == 'POST':
        parcel = get_object_or_404(Parcel, id=parcel_id, courier=request.user)
        
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        status = request.POST.get('status', parcel.status)
        description = request.POST.get('description', f'Location updated to ({latitude}, {longitude})')
        
        parcel.status = status
        parcel.save()
        
        TrackingEvent.objects.create(
            parcel=parcel,
            status=status,
            description=description,
            latitude=latitude,
            longitude=longitude
        )
        
        return JsonResponse({'success': True, 'message': 'Location updated'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from apps.parcels.models import Parcel
from .models import TrackingEvent


def track_parcel_view(request, tracking_number):
    parcel = get_object_or_404(Parcel, tracking_number=tracking_number)
    tracking_events = parcel.tracking_events.all().order_by('-timestamp')
    
    context = {
        'parcel': parcel,
        'tracking_events': tracking_events,
        'mapbox_token': 'pk.mapbox_demo_token'
    }
    return render(request, 'tracking/track.html', context)


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

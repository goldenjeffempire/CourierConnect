from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Parcel


def is_courier(user):
    return user.is_authenticated and user.role == 'courier'


@login_required
@user_passes_test(is_courier)
def dashboard_view(request):
    assigned_parcels = Parcel.objects.filter(courier=request.user).exclude(status='delivered').order_by('-created_at')
    delivered_count = Parcel.objects.filter(courier=request.user, status='delivered').count()
    
    context = {
        'assigned_parcels': assigned_parcels,
        'delivered_count': delivered_count,
    }
    return render(request, 'courier/dashboard.html', context)


@login_required
@user_passes_test(is_courier)
def accept_parcel(request, parcel_id):
    parcel = get_object_or_404(Parcel, id=parcel_id, status='assigned', courier__isnull=True)
    parcel.courier = request.user
    parcel.save()
    messages.success(request, f'Parcel {parcel.tracking_number} accepted')
    return redirect('courier:dashboard')

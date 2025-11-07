from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from apps.parcels.models import Parcel
from apps.users.models import User


def is_admin(user):
    return user.is_authenticated and user.role == 'admin'


@login_required
@user_passes_test(is_admin)
def dashboard_view(request):
    total_parcels = Parcel.objects.count()
    pending = Parcel.objects.filter(status='pending').count()
    in_transit = Parcel.objects.filter(status='in_transit').count()
    delivered = Parcel.objects.filter(status='delivered').count()
    
    total_couriers = User.objects.filter(role='courier').count()
    total_customers = User.objects.filter(role='customer').count()
    
    recent_parcels = Parcel.objects.select_related('customer', 'courier').order_by('-created_at')[:10]
    
    context = {
        'total_parcels': total_parcels,
        'pending': pending,
        'in_transit': in_transit,
        'delivered': delivered,
        'total_couriers': total_couriers,
        'total_customers': total_customers,
        'recent_parcels': recent_parcels,
    }
    return render(request, 'admin_panel/dashboard.html', context)

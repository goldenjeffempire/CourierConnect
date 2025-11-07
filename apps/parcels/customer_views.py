from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Parcel


@login_required
def dashboard_view(request):
    if request.user.role != 'customer':
        from django.contrib import messages
        from django.shortcuts import redirect
        messages.error(request, 'Access denied')
        return redirect('home')
    
    my_parcels = Parcel.objects.filter(customer=request.user).order_by('-created_at')
    
    context = {
        'my_parcels': my_parcels,
    }
    return render(request, 'customer/dashboard.html', context)

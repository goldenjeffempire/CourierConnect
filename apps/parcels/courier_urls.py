from django.urls import path
from . import courier_views

app_name = 'courier'

urlpatterns = [
    path('dashboard/', courier_views.dashboard_view, name='dashboard'),
    path('accept/<int:parcel_id>/', courier_views.accept_parcel, name='accept_parcel'),
]

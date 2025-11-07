from django.urls import path
from . import customer_views

app_name = 'customer'

urlpatterns = [
    path('dashboard/', customer_views.dashboard_view, name='dashboard'),
]

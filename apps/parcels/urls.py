from django.urls import path
from . import views

app_name = 'parcels'

urlpatterns = [
    path('create/', views.create_parcel_view, name='create'),
    path('quote/', views.get_quote_view, name='quote'),
    path('<str:tracking_number>/', views.parcel_detail_view, name='detail'),
    path('<str:tracking_number>/pay/', views.payment_view, name='payment'),
]

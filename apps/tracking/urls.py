from django.urls import path
from . import views

app_name = 'tracking'

urlpatterns = [
    path('<str:tracking_number>/', views.track_parcel_view, name='track'),
    path('update/<int:parcel_id>/', views.update_location_view, name='update_location'),
]

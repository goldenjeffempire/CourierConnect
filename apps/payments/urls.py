from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('webhook/stripe/', views.stripe_webhook_view, name='stripe_webhook'),
    path('success/', views.payment_success_view, name='success'),
    path('cancel/', views.payment_cancel_view, name='cancel'),
]

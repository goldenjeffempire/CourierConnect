from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('webhook/stripe/', views.stripe_webhook_view, name='stripe_webhook'),
    path('success/', views.payment_success_view, name='success'),
    path('cancel/', views.payment_cancel_view, name='cancel'),
    path('parcel/<int:parcel_id>/', views.payment_page_view, name='payment_page'),
    path('parcel/<int:parcel_id>/upload-proof/', views.upload_proof_of_payment_view, name='upload_proof'),
    path('<int:payment_id>/invoice/', views.download_invoice_view, name='download_invoice'),
    path('<int:payment_id>/receipt/', views.download_receipt_view, name='download_receipt'),
]

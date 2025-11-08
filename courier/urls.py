from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('contact/', TemplateView.as_view(template_name='contact.html'), name='contact'),
    path('auth/', include('apps.users.urls')),
    path('parcels/', include('apps.parcels.urls')),
    path('tracking/', include('apps.tracking.urls')),
    path('payments/', include('apps.payments.urls')),
    path('admin-panel/', include('apps.admin_panel.urls')),
    path('courier/', include('apps.parcels.courier_urls')),
    path('customer/', include('apps.parcels.customer_urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

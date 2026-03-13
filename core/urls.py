from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/whatsapp/', include('whatsapp_integration.urls')),
    path('api-auth/', include('rest_framework.urls')),
]
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from decouple import config


ADMIN_URL = config('ADMIN_URL', default='autoprime-secure-admin-2026/')

admin.site.site_header  = 'AutoPrime Motors Admin'
admin.site.site_title   = 'AutoPrime Admin Portal'
admin.site.index_title  = 'Inventory & Site Management'

urlpatterns = [
    path(ADMIN_URL, admin.site.urls),

    # Your AutoPrime homepage
    path('', include('home.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

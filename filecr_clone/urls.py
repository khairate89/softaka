# filecr_clone_django_project/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('nested_admin/', include('nested_admin.urls')),
    
    # IMPORTANT: Place the CKEditor URL include BEFORE your generic app include
    path('ckeditor/', include('ckeditor_uploader.urls')), # <--- THIS GOES FIRST!
    
    path('', include('software.urls')), # Your software app URLs come after specific ones
]

# Serve media files in development (IMPORTANT for uploaded images)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



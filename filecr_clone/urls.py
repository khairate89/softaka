# filecr_clone/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.http import HttpResponseRedirect
from django.conf import settings
from software import views as software_views # <--- ADD THIS LINE
# Import static for media file serving
from django.conf.urls.static import static
# Import staticfiles_urlpatterns for automatic static files serving in DEBUG mode
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

def redirect_to_language_prefix(request):
    """
    Redirects the root URL ('/') to the default language prefix (e.g., '/en/').
    """
    return HttpResponseRedirect(f'/{settings.LANGUAGE_CODE}/')

# Define the base urlpatterns for NON-TRANSLATED URLs FIRST
# These URLs will NOT have a language prefix and will NOT be translated
urlpatterns = [
    path('admin/', admin.site.urls), # MOVED OUTSIDE i18n_patterns
    path('nested_admin/', include('nested_admin.urls')), # MOVED OUTSIDE i18n_patterns
    path('ckeditor/', include('ckeditor_uploader.urls')), # MOVED OUTSIDE i18n_patterns
    path('i18n/', include('django.conf.urls.i18n')), # This always needs to be non-translated
    path('', redirect_to_language_prefix), # Catch-all for the root
     # --- YOU NEED TO ADD THIS LINE HERE: ---
    path('subscribe/', software_views.subscribe_newsletter, name='subscribe_newsletter'), 
    # --- END OF ADDITION ---
]

# Now, add the URLs that SHOULD be translated and have a language prefix
urlpatterns += i18n_patterns(
    path('', include('software.urls')), # This means /en/, /fr/, etc. for your app
    # Add other app URLs here that you want translated
)


# IMPORTANT: Serve static and media files ONLY when DEBUG is True.
# In production, these are served by a dedicated web server (Nginx/Apache).
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
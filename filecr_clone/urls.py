from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.http import HttpResponseRedirect
from django.conf import settings
from software import views as software_views
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.sitemaps.views import sitemap
from software.sitemaps import SoftwareSitemap, StaticViewSitemap, CategorySitemap


def redirect_to_language_prefix(request):
    """
    Redirects the root URL ('/') to the default language prefix (e.g., '/en/').
    """
    return HttpResponseRedirect(f'/{settings.LANGUAGE_CODE}/')


sitemaps = {
    'static': StaticViewSitemap,
    'software': SoftwareSitemap,
    'categories': CategorySitemap,
}

# Base urlpatterns for non-translated URLs
urlpatterns = [
    path('admin/', admin.site.urls),
    path('nested_admin/', include('nested_admin.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('', redirect_to_language_prefix),
    path('subscribe/', software_views.subscribe_newsletter, name='subscribe_newsletter'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

# Translated URLs with language prefix (e.g. /en/, /fr/)
urlpatterns += i18n_patterns(
    path('', include('software.urls')),
)

# Serve static and media files in development only
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

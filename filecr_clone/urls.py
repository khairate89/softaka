# filecr_clone/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.http import HttpResponseRedirect
from django.conf import settings
from software import views as software_views
from django.contrib.sitemaps.views import sitemap
from software.sitemaps import SoftwareSitemap, StaticViewSitemap, CategorySitemap
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


def redirect_to_language_prefix(request):
    return HttpResponseRedirect(f'/{settings.LANGUAGE_CODE}/')


sitemaps = {
    'static': StaticViewSitemap,      # class here — ✅ correct
    'software': SoftwareSitemap,      # class here — ✅ correct
    'categories': CategorySitemap,    # class here — ✅ correct
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('nested_admin/', include('nested_admin.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('', redirect_to_language_prefix),
    path('subscribe/', software_views.subscribe_newsletter, name='subscribe_newsletter'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

urlpatterns += i18n_patterns(
    path('', include('software.urls')),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

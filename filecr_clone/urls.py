# filecr_clone/urls.py

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.i18n import i18n_patterns
from django.http import HttpResponseRedirect
from django.conf import settings
from django.views.generic import TemplateView
from django.views.static import serve
from software import views as software_views

# Sitemap Imports
from django.contrib.sitemaps import views as sitemap_views
from software.sitemaps import SoftwareSitemap, StaticViewSitemap, CategorySitemap

# Static and Media Serving Imports
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


def redirect_to_language_prefix(request):
    """
    Redirects the root URL ('/') to the user's default language prefix (e.g., '/en/').
    """
    return HttpResponseRedirect(f'/{settings.LANGUAGE_CODE}/')


sitemaps = {
    'static': StaticViewSitemap,
    'software': SoftwareSitemap,
    'categories': CategorySitemap,
}

# --- PRIMARY URL PATTERNS ---
# These patterns are processed first and do NOT have a language prefix.
urlpatterns = [
    # Admin and common non-i18n apps
    path('admin/', admin.site.urls),
    path('nested_admin/', include('nested_admin.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),

    # The sitemap index URL and individual sitemap URLs.
    # These are handled by Django's built-in sitemap views.
    path('sitemap.xml', sitemap_views.index, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.index'),
    path('sitemap-<section>.xml', sitemap_views.sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    
    # Your non-translated subscribe endpoint
    path('subscribe/', software_views.subscribe_newsletter, name='subscribe_newsletter'),
]


# --- INTERNATIONALIZED URL PATTERNS ---
# These patterns get the language prefix (e.g., /en/, /fr/).
urlpatterns += i18n_patterns(
    # This maps the language root (e.g., /en/, /fr/) to your software app's URLs.
    path('', include('software.urls', namespace='software')),

    prefix_default_language=True,
)


# --- ROOT REDIRECT FOR BARE DOMAIN ---
# This special pattern must come after all other URL patterns.
urlpatterns += [
    path('', redirect_to_language_prefix, name='redirect_to_default_language'),
]


# --- STATIC AND MEDIA FILE SERVING (DEVELOPMENT ONLY) ---
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    # In a production environment, your web server (Nginx/Apache) would serve these static files.
    # This block is a fallback to handle any generated sitemap files from the management command.
    urlpatterns += [
        re_path(r'^(?P<path>sitemap-[a-z]{2}(-[a-z]{2})?\.xml)$', serve, {
            'document_root': settings.BASE_DIR / 'sitemaps',
        }),
    ]

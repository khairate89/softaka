# software/sitemaps.py

from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.conf import settings
from .models import Software

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        # Use namespaced view names
        return ['software:dmca', 'software:disclaimer', 'software:privacy_policy',
                'software:terms_conditions', 'software:sitemap_page',
                'software:contact_us', 'software:about_us']

    def location(self, item):
        return reverse(item)

    def alternates(self, item):
        alternates = []
        for lang_code, _ in settings.LANGUAGES:
            alternates.append({
                'lang': lang_code,
                'url': f'/{lang_code}{self.location(item)}'
            })
        return alternates


class SoftwareSitemap(Sitemap):
    priority = 0.9
    changefreq = 'weekly'

    def items(self):
        return Software.objects.all()

    def location(self, obj):
        # Default language URL
        lang_code = settings.LANGUAGE_CODE
        category_slug = getattr(obj.category, f'slug_{lang_code}', obj.category.slug)
        software_slug = getattr(obj, f'slug_{lang_code}', obj.slug)
        return f'/{lang_code}/{category_slug}/{software_slug}/'

    def alternates(self, obj):
        alternates = []
        for lang_code, _ in settings.LANGUAGES:
            category_slug = getattr(obj.category, f'slug_{lang_code}', obj.category.slug)
            software_slug = getattr(obj, f'slug_{lang_code}', obj.slug)
            url = f'/{lang_code}/{category_slug}/{software_slug}/'
            alternates.append({'lang': lang_code, 'url': url})
        return alternates

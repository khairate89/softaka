# software/sitemaps.py

from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.conf import settings
from .models import Software, Category

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return ['dmca', 'disclaimer']  # Add your static view names here

    def location(self, item):
        return reverse(item)

    def alternates(self, item):
        alternates = []
        for lang_code, lang_name in settings.LANGUAGES:
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
        # Example URL: /en/windows/test-software/
        return f'/{settings.LANGUAGE_CODE}/{obj.category.slug}/{obj.slug}/'

    def alternates(self, obj):
        alternates = []
        for lang_code, lang_name in settings.LANGUAGES:
            alternates.append({
                'lang': lang_code,
                'url': f'/{lang_code}/{obj.category.slug}/{obj.slug}/'
            })
        return alternates

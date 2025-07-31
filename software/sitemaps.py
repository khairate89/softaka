# software/sitemaps.py

from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from software.models import Software, Category

class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5
    # The i18n attribute is the key that tells Django to generate URLs for all languages.
    i18n = True

    def items(self):
        # We use the URL names here. The `location` method will reverse them.
        return [
             'software:home',
            'software:dmca',
            'software:disclaimer',
            'software:privacy_policy',
            'software:terms_conditions',
            'software:sitemap_page',
            'software:contact_us',
            'software:about_us',
        ]

    def location(self, item):
        # `reverse()` will automatically handle the language prefix because i18n_patterns is used.
        return reverse(item)


class SoftwareSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    # The i18n attribute is the key.
    i18n = True
    # The limit attribute, by default 1000, handles automatic pagination for large sites.
    # You can set it to a higher value if needed (up to 50000).
    limit = 1000 

    def items(self):
        # Good practice to filter for published items.
        return Software.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()


class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7
    # The i18n attribute is the key.
    i18n = True

    def items(self):
        # Good practice to filter for published categories.
        return Category.objects.filter(is_published=True)

    def lastmod(self, obj):
        if hasattr(obj, 'updated_at'):
            return obj.updated_at
        return None

    def location(self, obj):
        return obj.get_absolute_url()

from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.conf import settings
from django.utils.translation import activate, get_language

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        # Replace with your actual static page URL names (the names used in urls.py)
        return ['home', 'about-us', 'contact-us']

    def location(self, item):
        return reverse(item)

    def get_urls(self, site=None, **kwargs):
        urls = []
        original_language = get_language()
        for lang_code, _ in settings.LANGUAGES:
            activate(lang_code)
            for item in self.items():
                urls.append({
                    'location': self.location(item),
                    'priority': self.priority,
                    'changefreq': self.changefreq,
                    'lang': lang_code,
                })
        activate(original_language)
        return urls


class SoftwareSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        from software.models import Software  # Adjust this import as needed
        return Software.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        # Assumes get_absolute_url respects active language
        return obj.get_absolute_url()

    def get_urls(self, site=None, **kwargs):
        urls = []
        original_language = get_language()
        for lang_code, _ in settings.LANGUAGES:
            activate(lang_code)
            for obj in self.items():
                urls.append({
                    'location': self.location(obj),
                    'lastmod': self.lastmod(obj),
                    'priority': self.priority,
                    'changefreq': self.changefreq,
                    'lang': lang_code,
                })
        activate(original_language)
        return urls

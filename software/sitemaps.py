from django.contrib.sitemaps import Sitemap
from django.utils.translation import activate, get_language
from django.conf import settings
from django.contrib.sites.models import Site
from software.models import Software, Category

class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return ['home', 'about-us', 'contact-us']

    def location(self, item):
        return f'/{item}/'

    def get_urls(self, site=None, **kwargs):
        if site is None:
            site = Site.objects.get_current()
        domain = f'https://{site.domain}'

        urls = []
        original_language = get_language()
        for lang_code, _ in settings.LANGUAGES:
            activate(lang_code)
            for item in self.items():
                url = self.location(item)
                if not url.startswith(f'/{lang_code}/'):
                    url = f'/{lang_code}{url}'
                full_url = domain + url
                urls.append({
                    'location': full_url,
                    'changefreq': self.changefreq,
                    'priority': float(self.priority),
                    'lang': lang_code,
                })
        activate(original_language)
        return urls


class SoftwareSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Software.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()

    def get_urls(self, site=None, **kwargs):
        if site is None:
            site = Site.objects.get_current()
        domain = f'https://{site.domain}'

        urls = []
        original_language = get_language()
        for lang_code, _ in settings.LANGUAGES:
            activate(lang_code)
            for obj in self.items():
                url = self.location(obj)
                if not url.startswith(f'/{lang_code}/'):
                    url = f'/{lang_code}{url}'
                full_url = domain + url
                urls.append({
                    'location': full_url,
                    'lastmod': self.lastmod(obj),
                    'changefreq': self.changefreq,
                    'priority': float(self.priority),
                    'lang': lang_code,
                })
        activate(original_language)
        return urls


class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Category.objects.all()

    def lastmod(self, obj):
        if hasattr(obj, 'updated_at'):
            return obj.updated_at
        return None

    def location(self, obj):
        return obj.get_absolute_url()

    def get_urls(self, site=None, **kwargs):
        if site is None:
            site = Site.objects.get_current()
        domain = f'https://{site.domain}'

        urls = []
        original_language = get_language()
        for lang_code, _ in settings.LANGUAGES:
            activate(lang_code)
            for obj in self.items():
                url = self.location(obj)
                if not url.startswith(f'/{lang_code}/'):
                    url = f'/{lang_code}{url}'
                full_url = domain + url
                urls.append({
                    'location': full_url,
                    'lastmod': self.lastmod(obj),
                    'changefreq': self.changefreq,
                    'priority': float(self.priority),
                    'lang': lang_code,
                })
        activate(original_language)
        return urls

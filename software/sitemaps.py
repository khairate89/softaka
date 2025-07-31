from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Software, Category

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        # Add the names of your static views here, matching your URL names
        return ['home', 'about-us', 'contact-us']  # <--- update with your actual static page URL names

    def location(self, item):
        return reverse(item)


class SoftwareSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Software.objects.all()

    def lastmod(self, obj):
        return obj.updated_at


class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return Category.objects.all()

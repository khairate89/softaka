from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.conf import settings
from django.utils.translation import activate, get_language

class SoftwareSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Software.objects.all()

    def location(self, obj):
        return obj.get_absolute_url()

    def alternates(self, obj):
        alternates = []
        current_lang = get_language()
        for lang_code, _ in settings.LANGUAGES:
            if lang_code == current_lang:
                continue
            activate(lang_code)
            url = obj.get_absolute_url()
            alternates.append({
                'lang_code': lang_code,
                'url': url,
            })
        activate(current_lang)
        return alternates

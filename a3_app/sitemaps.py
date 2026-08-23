from urllib.parse import urlparse

from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .seo import SITE_URL

DOMAIN = urlparse(SITE_URL).netloc


class _CanonicalSite:
    """Pins sitemap URLs to the canonical domain, whatever host serves them."""
    domain = name = DOMAIN


class StaticViewSitemap(Sitemap):
    """Every public page, weighted so the homepage and about page lead."""
    protocol = 'https'

    PAGES = {
        'index':             (1.0, 'weekly'),
        'about':             (0.9, 'monthly'),
        'services':          (0.9, 'monthly'),
        'products':          (0.7, 'monthly'),
        'contact':           (0.8, 'monthly'),
        'sample':            (0.6, 'monthly'),
        'sample_gym':        (0.5, 'yearly'),
        'sample_restaurant': (0.5, 'yearly'),
        'sample_portfolio':  (0.5, 'yearly'),
        'sample_petshop':    (0.5, 'yearly'),
    }

    def get_urls(self, page=1, site=None, protocol=None):
        return super().get_urls(page=page, site=_CanonicalSite(), protocol=self.protocol)

    def items(self):
        return list(self.PAGES)

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return self.PAGES[item][0]

    def changefreq(self, item):
        return self.PAGES[item][1]

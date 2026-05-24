from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from core.models import Article


class HomePageSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 1.0
    protocol = 'https'

    def items(self):
        return ['index']

    def location(self, item):
        return reverse(item)


class StaticPagesSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.8
    protocol = 'https'

    def items(self):
        return ['about', 'insights']

    def location(self, item):
        return reverse(item)


class ServicePagesSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.9
    protocol = 'https'

    _slugs = [
        'e-commerce-development',
        'ai-powered-automation',
        'custom-crm-development',
    ]

    def items(self):
        return self._slugs

    def location(self, slug):
        return reverse('service_page', kwargs={'service_slug': slug})


class ArticleSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.75
    protocol = 'https'

    def items(self):
        return Article.objects.filter(is_published=True).order_by('-created_at')

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return reverse('article_detail', kwargs={'article_slug': obj.slug})

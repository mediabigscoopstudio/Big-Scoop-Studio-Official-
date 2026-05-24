from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from main import views
from main.sitemaps import HomePageSitemap, StaticPagesSitemap, ServicePagesSitemap, ArticleSitemap
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

_sitemaps = {
    'home': HomePageSitemap,
    'static': StaticPagesSitemap,
    'services': ServicePagesSitemap,
    'articles': ArticleSitemap,
}

urlpatterns = [
    path('sitemap.xml', sitemap, {'sitemaps': _sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='main/robots.txt', content_type='text/plain'), name='robots_txt'),
    path("",views.index,name='index'),
    path("about/", views.about, name='about'),
    path("thank-you", views.thank_you, name='thank_you'),
    path("services/<slug:service_slug>/", views.service_page, name='service_page'),
    path("services/<slug:service_slug>/lead/", views.service_page_lead, name='service_page_lead'),
    path("insights/", views.insights, name='insights'),
    path("insights/category/<slug:category_slug>/", views.insights, name='insights_by_category'),
    path("insights/<slug:article_slug>/", views.article_detail, name='article_detail'),
    path("privacy", views.privacy_policy, name='privacy_policy'),
    path("policy/terms.html", views.terms_conditions, name='terms_conditions'),
    path("leads/get-proposal/", views.get_proposal_lead, name='get_proposal_lead'),
    path("leads/book-call/", views.book_call_lead, name='book_call_lead'),
    path("newsletter/subscribe/", views.newsletter_subscribe, name='newsletter_subscribe'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

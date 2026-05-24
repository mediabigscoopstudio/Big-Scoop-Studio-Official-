from django.contrib import admin
from django.urls import path,include
from manager import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', include('core.urls')),
    path("signin",views.signin_view,name='signin'),
    path("logout",views.logout_view,name='logout'),
    
    path("",views.index,name='index'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
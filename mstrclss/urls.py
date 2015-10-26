"""mstrclss URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import TemplateView
from django.conf import settings
from mstrclss.settings import STATIC_ROOT
from  django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', TemplateView.as_view(template_name='templates/landing.html')),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^classes/', 'classes.views.index', name='class_index'),
    url(r'^classes/manage', 'classes.views.add_or_edit_class', name='class_manager')
]
urlpatterns += (
    url(r'^static/(.*)$', 'django.views.static.serve', {'document_root': STATIC_ROOT, 'show_indexes': True}),
)

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


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', TemplateView.as_view(template_name='templates/landing.html')),
    url(r'^logout/', 'classes.views.logout_view', name='logout'),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^classes/$', 'classes.views.index', {'user': True}, name='class_index'),
    url(r'^myclasses/$', 'classes.views.index', name='my_classes'),
    url(r'^classes/(?P<class_pk>[0-9]+)/$', 'classes.views.detail', name='class_detail'),
    url(r'^classes/(?P<class_pk>[0-9]+)/drop/(?P<user_pk>[0-9]+)/$', 'classes.views.drop', name='class_drop'),
    url(r'^classes/manage/$', 'classes.views.add_or_edit_class', name='class_manager'),
    url(r'^classes/manage/(?P<class_pk>[0-9]+)/$', 'classes.views.add_or_edit_class', name='class_edit'),
    url(r'^classes/manage/toggle_live/(?P<class_pk>[0-9]+)/$', 'classes.views.toggle_live', name='class_toggle_live'),
    url(r'^classes/manage/delete/(?P<class_pk>[0-9]+)/$', 'classes.views.delete_class', name='class_delete'),
]


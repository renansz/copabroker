# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'broker.views.home'),
    url(r'^book/(\w+)/$', 'broker.views.book'),
    url(r'^profile$', 'broker.views.profile'),
    #url(r'^profile$', 'broker.views.profile', name='profile'), 
    # url(r'^copabroker/', include('copabroker.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'CopaBroker.views.home', name='home'),
    # url(r'^CopaBroker/', include('CopaBroker.foo.urls')),
    url(r'^$', 'broker.views.home'),
    url(r'^book/(\w+)/$', 'broker.views.book'),
    url(r'^profile/$', 'broker.views.profile'),
    url(r'^login/$', 'broker.views.login_user')
)

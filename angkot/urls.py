from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^$', 'angkot.views.home', name='home'),
    url(r'^trayek/', include('angkot.trayek.urls')),
    url(r'^route/', include('angkot.route.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^route/', include('angkot.route.urls')),
    url(r'^account/', include('angkot.account.urls')),
    url(r'^page/', include('angkot.page.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^go/route/(?P<route_id>\d+)', 'angkot.route.views.open_route'),
    url(r'^$', RedirectView.as_view(url='/route/', permanent=False), name="index"),
)

# account shortcuts
urlpatterns += patterns('',
    url(r'^login/$', RedirectView.as_view(url='/account/login/', permanent=True)),
    url(r'^logout/$', RedirectView.as_view(url='/account/logout/', permanent=True)),
)


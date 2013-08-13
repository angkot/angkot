from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^route/', include('angkot.route.urls')),
    url(r'^account/', include('angkot.account.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', RedirectView.as_view(url='/route/', permanent=False)),
)


from django.conf.urls import patterns, url

urlpatterns = patterns('angkot.geo.webapi.views',
    url(r'^provinces\.json$', 'province_list', name="wapi_province_list"),
)


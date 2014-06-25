from django.conf.urls import patterns, url

urlpatterns = patterns('angkot.geo.webapi.views',
    url(r'^provinces\.json$', 'province_list', name="wapi_geo_province_list"),
    url(r'^cities\.json$', 'city_list', name="wapi_geo_city_list"),
)


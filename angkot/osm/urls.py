from django.conf.urls import patterns, url

urlpatterns = patterns('angkot.osm.views',
    url(r'^route\.html$', 'route_page', name='osm_route'),
    url(r'^data/(?P<zoom>\d+)/(?P<x>\d+)/(?P<y>\d+)\.json$', 'data', name='osm_data'),
)


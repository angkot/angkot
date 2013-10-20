from django.conf.urls import patterns, url

urlpatterns = patterns('angkot.osm.views',
    url(r'^data/(?P<zoom>\d+)/(?P<x>\d+)/(?P<y>\d+)\.json$', 'data', name='osm_data'),
)


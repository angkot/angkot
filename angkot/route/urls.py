from django.conf.urls import patterns, include, url

urlpatterns = patterns('angkot.route.views',
    url(r'^$', 'index', name='route_index'),
    url(r'^(?P<route_id>[A-Za-z0-9]+)/$', 'editor', name='route_editor'),
)


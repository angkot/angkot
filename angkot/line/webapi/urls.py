from django.conf.urls import patterns, url

urlpatterns = patterns('angkot.line.webapi.views',
    # Line
    url(r'^list.json$', 'line_list', name='wapi_line_list'),
    url(r'^new$', 'line_new', name='wapi_line_new'),
    url(r'^(?P<line_id>\d+)/$', 'line_update', name='wapi_line_update'),
    url(r'^(?P<line_id>\d+)/data.json$', 'line_data', name='wapi_line_data'),

    # Route
    url(r'^(?P<line_id>\d+)/new-route$', 'line_route_new', name='wapi_line_route_new'),
    url(r'^(?P<line_id>\d+)/(?P<route_id>\d+)/data.json$', 'line_route_data', name='wapi_line_route_data'),
    url(r'^(?P<line_id>\d+)/(?P<route_id>\d+)/$', 'line_route_update', name='wapi_line_route_update'),
)



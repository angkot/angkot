from django.conf.urls import patterns, url

urlpatterns = patterns('angkot.line.webapi.views',
    url(r'^(?P<line_id>\d+)\.json$', 'line_data', name="wapi_line_data"),
    url(r'^list\.json$', 'line_list', name="wapi_line_list"),
)


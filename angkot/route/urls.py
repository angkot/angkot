from django.conf.urls import patterns, url

urlpatterns = patterns('angkot.route.views',
    url(r'^$', 'index', name='route_index'),
    url(r'^submissions.json$', 'submission_list', name='route_submissions'),
    url(r'^provinces.json$', 'province_list', name='route_province_list'),
    url(r'^transportations.json$', 'transportation_list', name='route_transportation_list'),
    url(r'^transportation/(?P<tid>\d+)\.json$',
        'transportation_data', name='route_transportation_data'),
)


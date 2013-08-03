from django.conf.urls import patterns, url

urlpatterns = patterns('angkot.route.views',
    url(r'^$', 'index', name='route_index'),
    url(r'^submissions.json$', 'submission_list', name='route_submissions'),
    url(r'^provinces.json$', 'province_list', name='route_province_list'),
)


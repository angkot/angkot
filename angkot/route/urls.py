from django.conf.urls import patterns, url

urlpatterns = patterns('angkot.route.views',
    url(r'^$', 'index', name='route_index'),
    url(r'^submission-list.json$', 'submission_list', name='route_submission_list'),
    url(r'^province-list.json$', 'province_list', name='route_province_list'),
)


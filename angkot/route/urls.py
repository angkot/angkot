from django.conf.urls import patterns, url

urlpatterns = patterns('angkot.route.views',
    url(r'^$', 'index', name='route_index'),
)


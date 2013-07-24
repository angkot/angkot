from django.conf.urls import patterns, url

urlpatterns = patterns('angkot.trayek.views',
    url(r'^$', 'index', name='trayek_index'),
)


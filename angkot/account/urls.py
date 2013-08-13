from django.conf.urls import patterns, include, url

urlpatterns = patterns('angkot.account.views',
    url(r'^$', 'index', name='account_index'),
    url(r'^login/$', 'login_page', name='account_login_page'),
    url(r'^logout/$', 'logout_page', name='account_logout_page'),
)

urlpatterns += patterns('',
    url(r'', include('social_auth.urls')),
)


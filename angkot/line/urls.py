from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView

urlpatterns = patterns('',
    url(r'', TemplateView.as_view(template_name='line/index.html'),
        name='line_index'),
)


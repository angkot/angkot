from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('angkot.account.views',
    url(r'^faq$', TemplateView.as_view(template_name="page/faq.html"), name="page_faq"),
)
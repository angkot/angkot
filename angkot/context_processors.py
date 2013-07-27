from django.conf import settings

def configs(request):
    print 'blah'
    fields = ['GOOGLE_ANALYTICS_ID', 'GOOGLE_ANALYTICS_HOST',
              'GOOGLE_MAPS_KEY']
    return dict([(field, getattr(settings, field, None)) for field in fields])


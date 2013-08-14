from django.conf import settings

def configs(request):
    print 'blah'
    fields = ['GOOGLE_ANALYTICS_ID', 'GOOGLE_ANALYTICS_HOST',
              'USERVOICE_CODE', 'MAPBOX_KEY',
              'ANGKOT_CONTRIBUTOR_TERMS_URL',
              'ANGKOT_PRIVACY_POLICY_URL',]
    return dict([(field, getattr(settings, field, None)) for field in fields])


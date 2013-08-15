from django.conf import settings

def configs(request):
    fields = ['GOOGLE_ANALYTICS_ID', 'GOOGLE_ANALYTICS_HOST',
              'GOOGLE_ANALYTICS_IGNORE',
              'USERVOICE_CODE', 'MAPBOX_KEY', 'BING_MAPS_KEY',
              'ANGKOT_CONTRIBUTOR_TERMS_URL',
              'ANGKOT_PRIVACY_POLICY_URL',]
    data = dict([(field, getattr(settings, field, None)) for field in fields])

    fields = [('GOOGLE_ANALYTICS_IGNORE', False),]
    data.update(dict([(field, getattr(settings, field, default))
                      for field, default in fields
                      if field not in data]))

    return data


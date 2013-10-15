from django.conf import settings

def test_debug():
    assert settings.DEBUG == False
    assert settings.TEMPLATE_DEBUG == False

def test_api_keys():
    assert settings.GOOGLE_ANALYTICS_ID == 'UA-00000000-1'
    assert settings.GOOGLE_ANALYTICS_HOST == 'angkot.web.id'
    assert settings.MAPBOX_KEY == 'mapbox-key'
    assert settings.BING_MAPS_KEY == 'bingmaps-key'

def test_misc():
    assert settings.USERVOICE_CODE == 'uservoice-code'

    assert 'angkot.web.id' in settings.ALLOWED_HOSTS \
           or '*' in settings.ALLOWED_HOSTS

def test_oauth_keys():
    assert settings.GOOGLE_OAUTH2_CLIENT_ID == 'google-oauth2-client-id'
    assert settings.GOOGLE_OAUTH2_CLIENT_SECRET == 'google-oauth2-client-secret'

    assert settings.FACEBOOK_APP_ID == 'facebook-app-id'
    assert settings.FACEBOOK_API_SECRET == 'facebook-api-secret'

    assert settings.TWITTER_CONSUMER_KEY == 'twitter-consumer-key'
    assert settings.TWITTER_CONSUMER_SECRET == 'twitter-consumer-secret'


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
    assert settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY == 'google-oauth2-client-id'
    assert settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET == 'google-oauth2-client-secret'

    assert settings.SOCIAL_AUTH_FACEBOOK_KEY == 'facebook-app-id'
    assert settings.SOCIAL_AUTH_FACEBOOK_SECRET == 'facebook-api-secret'

    assert settings.SOCIAL_AUTH_TWITTER_KEY == 'twitter-consumer-key'
    assert settings.SOCIAL_AUTH_TWITTER_SECRET == 'twitter-consumer-secret'


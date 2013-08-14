from django.conf import settings

from social_auth.middleware import SocialAuthExceptionMiddleware
from social_auth.utils import backend_setting, get_backend_name

class AngkotSocialAuthExceptionMiddleware(SocialAuthExceptionMiddleware):
    def get_redirect_uri(self, request, exception):
        url = settings.LOGIN_ERROR_URL
        if self.backend is not None:
            url = backend_setting(self.backend,
                                  'SOCIAL_AUTH_BACKEND_ERROR_URL') or \
                                  settings.LOGIN_ERROR_URL

        url += '?e=%s' % exception.__class__.__name__
        if self.backend is not None:
            backend_name = get_backend_name(self.backend)
            url += '&b=%s' % backend_name

        return url


from django.conf import settings

from social.apps.django_app.middleware import SocialAuthExceptionMiddleware

class AngkotSocialAuthExceptionMiddleware(SocialAuthExceptionMiddleware):
    def get_redirect_uri(self, request, exception):
        backend_name = self.strategy.backend.name

        url = self.strategy.setting('LOGIN_ERROR_URL')
        url += '?e=%s&b=%s' % (exception.__class__.__name__, backend_name)

        return url


import logging

from .utils import log_extra

class ExceptionLoggerMiddleware(object):
    log = logging.getLogger('angkot.middleware.ExceptionLoggerMiddleware')

    def process_exception(self, request, exception):
        _e = log_extra(request)
        self.log.error(str(exception), exc_info=True, extra=_e)


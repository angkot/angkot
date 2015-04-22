from datetime import datetime

from django.http import HttpResponse

import json

__all__ = ('endpoint', )

class Response(object):
    def __init__(self):
        self.headers = {}

    def __setitem__(self, key, value):
        self.headers[key] = value

    def __getitem__(self, key):
        return self.headers[key]

class OK(Response):
    def __init__(self, data, http_code=200):
        super(OK, self).__init__()

        self.data = data
        self.http_code = http_code

    @property
    def dict(self):
        data = dict(self.data)
        data['status'] = 'ok'
        return data

class Fail(Response):
    def __init__(self, data=None, http_code=500,
                       error_code=500, error_msg="Internal server error"):
        super(Fail, self).__init__()

        if data is None:
            data = {}
        self.data = data
        self.http_code = http_code
        self.error_code = error_code
        self.error_msg = error_msg

    @property
    def dict(self):
        data = dict(self.data)
        data['status'] = 'fail'
        data['code'] = self.error_code
        data['msg'] = self.error_msg
        return data

class DateTimeJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super(DateTimeJsonEncoder, self).default(obj)

def encode_json(obj):
    encoder = DateTimeJsonEncoder(separators=(',',':'))
    return encoder.encode(obj)

def endpoint(func):
    def _func(request, *args, **kwargs):
        res = func(request, *args, **kwargs)
        code = 200
        headers = {}

        if res is None:
            data = {'status': 'ok'}

        elif type(res) == dict:
            data = dict(res)
            data['status'] = 'ok'

        elif isinstance(res, OK):
            data = res.dict
            code = res.http_code
            headers = res.headers

        elif isinstance(res, Fail):
            data = res.dict
            code = res.http_code
            headers = res.headers

        else:
            code = 500
            data = {'status': 'fail',
                    'code': 501,
                    'msg': 'Internal server error'}

        data = encode_json(data)
        res = HttpResponse(data, status=code, content_type='text/plain')
        for key, value in list(headers.items()):
            res[key] = value
        return res

    return _func


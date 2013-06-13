class OK(object):
    def __init__(self, data, http_code=200):
        self.data = data
        self.http_code = http_code

    @property
    def dict(self):
        data = dict(self.data)
        data['status'] = 'ok'
        return data

class Fail(object):
    def __init__(self, data=None, http_code=500,
                       error_code=500, error_msg="Internal server error"):
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

def api(func):
    from django.http import HttpResponse

    import json

    def _func(request, *args, **kwargs):
        res = func(request, *args, **kwargs)
        code = 200

        if res is None:
            data = {'status': 'ok'}

        elif type(res) == dict:
            data = dict(res)
            data['status'] = 'ok'

        elif isinstance(res, OK):
            data = res.dict
            code = res.http_code

        elif isinstance(res, Fail):
            data = res.dict
            code = res.http_code

        else:
            code = 500
            data = {'status': 'fail',
                    'code': 501,
                    'msg': 'Internal server error'}

        data = json.dumps(data)
        return HttpResponse(data, status=code, content_type='text/plain')

    return _func


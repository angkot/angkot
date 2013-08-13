class APIResponse(object):
    def __init__(self):
        self.headers = {}

    def __setitem__(self, key, value):
        self.headers[key] = value

    def __getitem__(self, key):
        return self.headers[key]

class OK(APIResponse):
    def __init__(self, data, http_code=200):
        super(OK, self).__init__()

        self.data = data
        self.http_code = http_code

    @property
    def dict(self):
        data = dict(self.data)
        data['status'] = 'ok'
        return data

class Fail(APIResponse):
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

def api(func):
    from django.http import HttpResponse

    import json

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

        data = json.dumps(data)
        res = HttpResponse(data, status=code, content_type='text/plain')
        for key, value in headers.items():
            res[key] = value
        return res

    return _func

def post_only(func):
    def _func(request, *args, **kwargs):
        if request.method != 'POST':
            return Fail(http_code=405, error_code=405,
                        error_msg='Method not allowed')

        return func(request, *args, **kwargs)

    return _func

def login_required(func):
    from django.http import HttpResponseRedirect
    from django.core.urlresolvers import reverse

    def _func(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('account_login_page'))
        return func(request, *args, **kwargs)
    return _func


def api(func):
    from django.http import HttpResponse

    import json

    def _func(request, *args, **kwargs):
        res = func(request, *args, **kwargs)
        code = 200

        if type(res) == dict:
            res['status'] = 'ok'
        elif type(res) == tuple:
            status = res[0]

            if status and len(res) > 1 \
               and type(res[1]) == dict:
                res = res[1]
                res['status'] = 'ok'
            elif not status and len(res) > 2 \
                 and type(res[1]) == int and type(res[2]) == dict:
                res = dict(res[2])
                res['status'] = 'fail'
                code = res[1]
            else:
                code = 501
                res = {'status': 'fail',
                       'code': 501,
                       'msg': 'Internal server error'}

        data = json.dumps(res)
        return HttpResponse(data, status=code, content_type='text/plain')

    return _func


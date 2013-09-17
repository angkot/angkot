from angkot import decorators as dec

data = {'foo': 'bar'}

def test_apiresponse_init():
    api = dec.APIResponse()
    assert api.headers == {}

def test_apiresponse_dict():
    api = dec.APIResponse()
    api['foo'] = 'bar'
    assert api.headers['foo'] == 'bar'


def test_ok_init():
    ok = dec.OK('data', http_code=1)
    assert ok.data == 'data'
    assert ok.http_code == 1

def test_ok_dict():
    ok = dec.OK(data)
    data.update({'status': 'ok'})
    assert ok.dict == data

def test_fail_init():
    fail = dec.Fail(data=data, http_code=1, error_code=0, error_msg='msg')
    assert fail.data == data
    assert fail.http_code == 1
    assert fail.error_code == 0
    assert fail.error_msg == 'msg'

def test_fail_init_nodata():
    fail = dec.Fail()
    assert fail.data == {}

def test_fail_dict():
    fail = dec.Fail(data=data, http_code=1, error_code=0, error_msg='msg')
    data.update(
        {
            'status': 'fail',
            'code': fail.error_code,
            'msg': fail.error_msg,
        }
    )
    assert fail.dict == data

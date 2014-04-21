from django.http import HttpResponse

from angkot.common.decorators import wapi

@wapi.endpoint
def line_list(req):
    return dict(lines=[])

@wapi.endpoint
def line_data(req, line_id):
    line_id = int(line_id)
    return dict(line_id=line_id,
                routes=[])


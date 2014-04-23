from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from angkot.common.utils import gpolyencode
from angkot.common.decorators import wapi

from ..models import Line

def _line_to_dict(item):
    return dict(id=item.id,
                label=item.label,
                name=item.name,
                mode=item.mode,
                province=item.province,
                city=item.city)

def _encode_path(path):
    if path is None:
        return None

    return gpolyencode.encode(path)

def _route_to_dict(item):
    return dict(id=item.id,
                name=item.name,
                locations=item.locations,
                ordering=item.ordering,
                path=_encode_path(item.path))

@wapi.endpoint
def line_list(req):
    data = Line.objects.filter(enabled=True)

    lines = list(map(_line_to_dict, data))
    return dict(lines=lines)

@wapi.endpoint
def line_data(req, line_id):
    line_id = int(line_id)

    line = get_object_or_404(Line, pk=line_id)
    routes = line.route_set.filter(enabled=True)

    line = _line_to_dict(line)
    routes = list(map(_route_to_dict, routes))

    return dict(id=line_id,
                line=line,
                routes=routes)


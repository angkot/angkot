import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.gis.geos import GEOSGeometry

from angkot.common.utils import gpolyencode, get_or_none, set_model_values
from angkot.common.decorators import wapi
from angkot.geo.utils import get_or_create_city
from angkot.geo.models import Province

from ..models import Line, Route, Author

def _line_to_dict(item):
    pid, cid = None, None
    city, province = None, None
    if item.city is not None:
        cid = item.city.id
        pid = item.city.province.id
        city = item.city.name
        province = item.city.province.name

    return dict(id=item.id,
                type=item.type,
                number=item.number,
                name=item.name,
                mode=item.mode,
                pid=pid,
                cid=cid,
                city=city,
                province=province)

def _line_to_pair(item):
    return (item.id, _line_to_dict(item))

def _encode_path(path):
    if path is None:
        return None

    return gpolyencode.encode(path)

def _route_to_dict(item):
    return dict(rid=item.id,
                lid=item.line.id,
                name=item.name,
                locations=item.locations,
                ordering=item.ordering,
                path=_encode_path(item.path),
                created=item.created,
                updated=item.updated)

def _get_line_params(raw_data):
    data = json.loads(raw_data)
    params = dict()

    # Acceptable fields
    for field in ['pid', 'city', 'number', 'type', 'name', 'mode']:
        if field in data:
            params[field] = data[field]

    # Mandatory fields
    for field in ['pid', 'city', 'number']:
        if params.get(field) is None:
            raise wapi.BadRequest()

    # Data type
    try:
        params['pid'] = int(params['pid'])
    except ValueError:
        raise wapi.BadRequest()

    # Province
    province = get_or_none(Province, pk=params['pid'])
    if province is None:
        raise wapi.BadRequest()

    # City
    params['city'] = get_or_create_city(province, params['city'])

    return params

def _line_data(req, line_id):
    line = get_object_or_404(Line, pk=int(line_id), enabled=True)
    routes = line.route_set.filter(enabled=True)

    line = _line_to_dict(line)
    routes = dict(map(_route_to_dict, routes))

    return dict(lid=line_id,
                line=line,
                routes=routes)

@wapi.get
def line_list(req):
    limit = 500

    try:
        page = int(req.GET.get('page', 0))
        cid = int(req.GET.get('cid', 0))
        pid = int(req.GET.get('pid', 0))
    except ValueError:
        page = 0
        cid = 0
        pid = 0

    filters = {}
    if cid > 0:
        filters['city__pk'] = cid
    elif pid > 0:
        filters['city__province__pk'] = pid

    start = page * limit
    end = start + limit
    query = Line.objects.filter(enabled=True, **filters) \
                        .order_by('pk')
    data = query[start:end]
    total = len(query)

    lines = dict(map(_line_to_pair, data))
    return dict(lines=lines,
                page=page,
                count=len(lines),
                total=total)

@wapi.post
def line_new(req):
    params = _get_line_params(req.POST)

    line = Line(**params)
    line.author = Author.objects.create_from_request(req)
    line.enabled = True
    line.save()

    return _line_data(line.id)

@wapi.get
def line_data(req, line_id):
    return _line_data(req, line_id)

@wapi.post
def line_update(req, line_id):
    line = get_object_or_404(Line, pk=int(line_id), enabled=True)

    params = _get_line_params(req.POST)
    set_model_values(line, params)
    line.author = Author.objects.create_from_request(req)
    line.save()

    return _line_data(line.id)

#
# Route
#

def _get_route_params(raw_data):
    data = json.loads(raw_data)

    params = dict()
    for field in ['name', 'ordering', 'locations', 'path']:
        if field in data:
            params[field] = data[field]

    if 'path' in params:
        params['path'] = GEOSGeometry(json.dumps(params['params']))
    if 'locations' in params:
        if type(params['locations']) != list:
            params['locations'] = [params['locations']]

    return params

def _line_route_data(req, line_id, route_id):
    route = get_object_or_404(Route, enabled=True,
                              pk=int(route_id), line__pk=int(line_id))

    return _route_to_dict(route)

@wapi.post
def line_route_new(req, line_id):
    line = get_object_or_404(Line, pk=int(line_id), enabled=True)

    params = _get_route_params(req.POST['data'])
    route = Route(line=line, **params)
    route.author = Author.objects.create_from_request(req)
    route.enabled = True
    route.save()

    return _line_route_data(req, line_id, route.id)

@wapi.get
def line_route_data(req, line_id, route_id):
    return _line_route_data(req, line_id, route_id)

@wapi.post
def line_route_update(req, line_id, route_id):
    route = get_object_or_404(Route, enabled=True,
                              pk=int(route_id), line__pk=int(line_id))

    params = _get_route_params(req)
    set_model_values(route, params)
    route.author = Author.objects.create_from_request(req)
    route.save()

    return _line_route_data(req, line_id, route.id)


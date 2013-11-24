from collections import defaultdict

from django.conf import settings
from django.contrib.gis.gdal import SpatialReference, CoordTransform
from django.contrib.gis.geos import Point
from django.contrib.gis.geos import Polygon
from django.http import HttpResponse, Http404
from django.views.decorators.cache import cache_page

from .utils import num2deg
from .models import Node, Way, WayNode
from angkot.decorators import api, OK

CT = CoordTransform(SpatialReference(4326),
                    SpatialReference(3857))

def route_page(request):
    from django.shortcuts import render_to_response
    from django.template import RequestContext
    print 'a'
    return render_to_response('osm/route.html',
                              context_instance=RequestContext(request))

@cache_page(24 * 60 * 60)
@api
def data(request, zoom, x, y):
    zoom, x, y = map(int, [zoom, x, y])
    if zoom < settings.OSM_QUERY_MIN_LEVEL:
        raise Http404()

    c1 = num2deg(x, y, zoom)
    c2 = num2deg(x+1, y+1, zoom)
    y1, x1 = c1
    y2, x2 = c2
    x1, x2 = min(x1, x2), max(x1, x2)
    y1, y2 = min(y1, y2), max(y1, y2)

    coords = ((x1, y1), (x2, y1), (x2, y2), (x1, y2), (x1, y1))
    geom = 'POLYGON ((%s))' % ', '.join(['%s %s' % coord
                                       for coord in coords])
    sql = '''
        WITH
            selected_nodes AS (
                SELECT id
                FROM osm_node
                WHERE ST_Contains(ST_GeomFromText('%s', 4326), coord)
            ),
            ways AS (
                SELECT DISTINCT way_id
                FROM osm_waynode
                WHERE node_id IN (SELECT id FROM selected_nodes)
            ),
            nodes AS (
                SELECT DISTINCT node_id
                FROM osm_waynode
                WHERE way_id IN (SELECT way_id FROM ways)
            )
        SELECT id, osm_id, coord
        FROM osm_node
        WHERE id IN (SELECT node_id FROM nodes)
    ''' % geom
    nodes = Node.objects.raw(sql)

    sql = '''
        WITH
            selected_nodes AS (
                SELECT id
                FROM osm_node
                WHERE ST_Contains(ST_GeomFromText('%s', 4326), coord)
            ),
            ways AS (
                SELECT DISTINCT way_id
                FROM osm_waynode
                WHERE node_id IN (SELECT id FROM selected_nodes)
            )
        SELECT id, way_id, node_id
        FROM osm_waynode
        WHERE way_id IN (SELECT way_id FROM ways)
        ORDER BY way_id, index
    ''' % geom
    ways = WayNode.objects.raw(sql)

    ids = []
    osm_ids = []
    latlngs = []
    for node in nodes:
        ids.append(node.id)
        osm_ids.append(node.osm_id)
        latlngs.append((node.coord.y, node.coord.x))

    way_list = defaultdict(list)
    for s in ways:
        way_list[s.way_id].append(s.node_id)

    way_highway = Way.objects.filter(pk__in=way_list.keys()) \
                                     .values_list('pk', 'highway')

    data = dict(x=x, y=y, zoom=zoom,
                bbox=[(x1,y1), (x2, y2)],
                nodes=dict(ids=ids, osm_ids=osm_ids, latlngs=latlngs),
                ways=way_list,
                ways_highway=dict(way_highway))
    return OK(data)


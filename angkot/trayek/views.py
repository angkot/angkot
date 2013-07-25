from django.shortcuts import render_to_response
from django.template import RequestContext

from angkot.decorators import api

@api
def _save_route(request):
    import geojson
    from shapely.geometry import asShape

    data = request.POST['geojson']
    data = geojson.loads(data, object_hook=geojson.GeoJSON.to_instance)
    print data.extra
    data = asShape(data)
    print data.wkt

def index(request):
    print 'Method:', request.method
    if request.method == 'POST':
        return _save_route(request)

    return render_to_response('trayek/trayek.html',
                              context_instance=RequestContext(request))


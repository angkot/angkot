from django.shortcuts import render_to_response
from django.template import RequestContext

from angkot.decorators import api, OK
from .models import Submission

@api
def _save_route(request):
    import geojson
    from shapely.geometry import asShape

    raw = request.POST['geojson']
    parent_id = request.POST.get('parent_id', None)
    try:
        parent = Submission.objects.get(submission_id=parent_id)
    except Submission.DoesNotExist:
        parent = None

    submission = Submission()
    submission.parent = parent
    submission.visitor_id = request.session['visitor-id']
    submission.ip_address = request.META['REMOTE_ADDR']
    submission.user_agent = request.META['HTTP_USER_AGENT']
    submission.raw_geojson = raw
    submission.save()

    data = geojson.loads(raw, object_hook=geojson.GeoJSON.to_instance)
    properties = data.extra['properties']
    wkt = asShape(data).wkt

    submission.rute = wkt
    submission.save()

    data = dict(submission_id=submission.submission_id)
    res = OK(data, http_code=201)
    res['Location'] = '/trayek/+%s/' % submission.submission_id
    return res

def index(request):
    print 'Method:', request.method
    if request.method == 'POST':
        return _save_route(request)

    return render_to_response('trayek/index.html',
                              context_instance=RequestContext(request))


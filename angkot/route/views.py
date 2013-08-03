from django.shortcuts import render_to_response
from django.template import RequestContext

from angkot.decorators import api, OK, Fail
from .models import Submission, PROVINCES
from .submission.data import process as processSubmission

@api
def _save_route(request):
    import geojson
    from shapely.geometry import asShape

    raw = request.POST['geojson']
    print raw
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

    processSubmission(submission)
    submission.save()

    data = dict(submission_id=submission.submission_id)
    if submission.parsed_ok:
        res = OK(data, http_code=201)
        res['Location'] = '/trayek/+%s/' % submission.submission_id
    else:
        res = Fail(data, http_code=400,
                   error_code=400, error_msg='Invalid data')
    return res

def index(request):
    if request.method == 'POST':
        return _save_route(request)
    return render_to_response('route/index.html',
                              context_instance=RequestContext(request))

@api
def submission_list(request):
    batch = 25
    start = int(request.GET.get('start', 0))

    items = Submission.objects.filter(active=True)
    items = items[start:start+batch]

    def format_item(item):
        return dict(created=int(item.created.strftime("%s")),
                    geojson=item.to_geojson())

    submissions = [format_item(item) for item in items]

    data = dict(submissions=submissions)
    return OK(data)

@api
def province_list(request):
    return dict(provinces=PROVINCES)


import json

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db import transaction
from django.core.urlresolvers import resolve

from angkot.decorators import api, OK, Fail, post_only
from .models import Transportation, Submission, PROVINCES
from .submission.data import process as processSubmission
from .forms import NewTransportationForm
from . import utils

def _format_date(d):
    return d.strftime('%s')

@api
def _new_transportation(request):
    f = NewTransportationForm(request.POST)
    if not f.is_valid():
        return Fail(http_code=400, error_code=400,
                    error_msg='Request requires province, city, and number; ' \
                              'and accept the contributor terms')

    province = f.cleaned_data['province']
    city = f.cleaned_data['city']
    number = f.cleaned_data['number']

    code = 200
    submission_id = None
    with transaction.commit_on_success():
        s = Submission()
        s.visitor_id = request.session['visitor-id']
        s.ip_address = request.META['REMOTE_ADDR']
        s.user_agent = request.META['HTTP_USER_AGENT']
        s.user = request.user
        s.raw_geojson = json.dumps(utils.create_geojson_feature(
            province=province,
            city=city,
            number=number,
            agreeToContributorTerms=True))
        s.save()

        items = Transportation.objects.filter(active=True, province=province,
                                              city=city, number=number)

        assert len(items) in [0, 1]
        if len(items) > 0:
            t = items[0]
        else:
            t = Transportation(active=True, province=province,
                               city=city, number=number)
            t.save()

            s.transportation = t
            s.save()

            code = 201

    data = dict(id=t.id,
                province=t.province,
                city=t.city,
                number=t.number,
                submission_id=s.submission_id)

    return OK(data, code)

def index(request):
    if request.method == 'POST':
        return _new_transportation(request)
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

@api
def transportation_list(request):
    # TODO cache this
    def format_transportation(t):
        return dict(id=t.id,
                    province=t.province,
                    city=t.city,
                    company=t.company,
                    number=t.number,
                    origin=t.origin,
                    destination=t.destination,
                    created=_format_date(t.created),
                    updated=_format_date(t.updated))

    items = Transportation.objects.filter(active=True)
    transportations = map(format_transportation, items)

    return dict(provinces=PROVINCES,
                transportations=transportations)

@api
def transportation_data(request, tid):
    tid = int(tid)
    t = Transportation.objects.get(pk=tid)

    return dict(id=t.id,
                geojson=t.to_geojson(),
                created=_format_date(t.created),
                updated=_format_date(t.updated))

@api
@post_only
def transportation_data_save(request, tid):
    import geojson
    from shapely.geometry import asShape

    tid = int(tid)
    t = Transportation.objects.get(pk=tid)

    raw = request.POST['geojson']
    print raw
    parent_id = request.POST.get('parent_id', None)
    try:
        parent = Submission.objects.get(submission_id=parent_id)
    except Submission.DoesNotExist:
        parent = None

    s = Submission()
    s.parent = parent
    s.visitor_id = request.session['visitor-id']
    s.ip_address = request.META['REMOTE_ADDR']
    s.user_agent = request.META['HTTP_USER_AGENT']
    s.user = request.user
    s.raw_geojson = raw
    s.save()

    processSubmission(s)
    if s.parsed_ok:
        s.transportation = t
    s.save()

    if s.parsed_ok:
        # Update transportation
        # province, city, and number are not updated from here
        t.company = s.company
        t.origin = s.origin
        t.destination = s.destination
        t.route = s.route
        t.save()

    data = dict(submission_id=s.submission_id)
    if s.parsed_ok:
        res = OK(data, http_code=201)
    else:
        res = Fail(data, http_code=400,
                   error_code=400, error_msg='Invalid data')
    return res


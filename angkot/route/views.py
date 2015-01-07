import json
import logging

from django.core.urlresolvers import resolve
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.cache import cache_page

from angkot.decorators import api, OK, Fail, api_post_only, api_login_required
from angkot.route import utils
from angkot.route.forms import NewTransportationForm
from angkot.route.models import Transportation, Submission, PROVINCES
from angkot.route.submission.data import process as processSubmission
from angkot.utils import log_extra

log = logging.getLogger(__name__)

def _format_date(d):
    return d.strftime('%s')

@api
@api_login_required
def _new_transportation(request):
    _e = log_extra(request)

    f = NewTransportationForm(request.POST)
    if not f.is_valid():
        log.error('new transportation: incomplete data', extra=_e)
        return Fail(http_code=400, error_code=400,
                    error_msg='Request requires province, city, and number; ' \
                              'and accept the contributor terms')

    province = f.cleaned_data['province']
    city = f.cleaned_data['city']
    number = f.cleaned_data['number']
    company = f.cleaned_data['company']

    city = utils.capwords(city)
    if company is not None:
        company = utils.capwords(company)

    code = 200
    submission_id = None
    with transaction.commit_on_success():
        s = Submission()
        s.ip_address = request.META['REMOTE_ADDR']
        s.user_agent = request.META['HTTP_USER_AGENT']
        s.user = request.user
        s.raw_geojson = json.dumps(utils.create_geojson_feature(
            province=province,
            city=city,
            number=number,
            company=company,
            agreeToContributorTerms=True))
        s.source = 'web'
        processSubmission(s)
        s.save()

        items = Transportation.objects.filter(active=True, province=province,
                                              city=city, number=number)

        assert len(items) in [0, 1]
        if len(items) > 0:
            t = items[0]
        else:
            t = Transportation(active=True, province=province,
                               city=city, number=number, company=company)
            t.save()

            s.transportation = t
            s.save()

            code = 201

        s.transportation = t
        s.save()

        log.info('new transportation: added: sid=%d tid=%d', s.id, t.id, extra=_e)

    data = dict(id=t.id,
                province=t.province,
                city=t.city,
                number=t.number,
                company=t.company,
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

@cache_page(24 * 60 * 60)
def province_list_js(request):
    data = dict(provinces=json.dumps(PROVINCES))
    return render_to_response('route/province-list.js', data,
                              content_type='text/javascript',
                              context_instance=RequestContext(request))

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
                    updated=_format_date(t.updated),
                    hasRoute=t.route is not None)

    def parse_ids(ids):
        return [int(tid) for tid in ids
                         if tid.isdigit()]

    extra_filters = dict()
    if 'id' in request.GET:
        ids = request.GET['id'].split('|')[:250]
        ids = parse_ids(ids)
        extra_filters['id__in'] = ids

    items = Transportation.objects.filter(active=True) \
                                  .filter(**extra_filters)
    transportations = list(map(format_transportation, items))

    return dict(provinces=PROVINCES,
                transportations=transportations)

@api
def transportation_data(request, tid):
    tid = int(tid)
    try:
        t = Transportation.objects.get(pk=tid, active=True)
    except Transportation.DoesNotExist:
        return Fail(http_code=404, error_code=404,
                    error_msg='Unknown transportation id: {}'.format(tid))

    sid = None
    if t.submission is not None:
        sid = t.submission.submission_id

    return dict(id=t.id,
                submission_id=sid,
                geojson=t.to_geojson(),
                created=_format_date(t.created),
                updated=_format_date(t.updated))

@api
@api_post_only
@api_login_required
def transportation_data_save(request, tid):
    _e = log_extra(request)

    tid = int(tid)
    try:
        t = Transportation.objects.get(pk=tid)
    except Transportation.DoesNotExist:
        log.error('save transportation: invalid id: tid=%s', tid, extra=_e)
        return Fail(http_code=404, error_code=404,
                    error_msg='Unknown transportation id: {}'.format(tid))

    raw = request.POST['geojson']
    parent_id = request.POST.get('parent_id', None)

    log.info('save transportation: received data: parent=%s geojson=%s',
             parent_id, raw, extra=_e)

    try:
        parent = Submission.objects.get(submission_id=parent_id)
    except Submission.DoesNotExist:
        parent = None

    s = Submission()
    s.parent = parent
    s.ip_address = request.META['REMOTE_ADDR']
    s.user_agent = request.META['HTTP_USER_AGENT']
    s.user = request.user
    s.raw_geojson = raw
    s.source = 'web'
    s.save()

    processSubmission(s)
    if s.parsed_ok:
        s.transportation = t
        s.city = utils.capwords(s.city)
        if s.company is not None:
            s.company = utils.capwords(s.company)
    s.save()

    if s.parsed_ok:
        # Update transportation
        t.province = s.province
        t.city = s.city
        t.company = s.company
        t.number = s.number
        t.origin = s.origin
        t.destination = s.destination
        t.route = s.route
        t.submission = s
        t.save()
        log.info('save transportation: saved: sid=%d tid=%d', s.id, t.id, extra=_e)

    else:
        log.info('save transportation: invalid data: sid=%d', s.id, extra=_e)

    data = dict(submission_id=s.submission_id)
    if s.parsed_ok:
        res = OK(data, http_code=201)
    else:
        res = Fail(data, http_code=400,
                   error_code=400, error_msg='Invalid data')
    return res

def open_route(request, route_id):
    path = '/route/#/{}/'.format(route_id)
    return HttpResponseRedirect(path)


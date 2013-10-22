from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

def is_valid_province(code):
    from ...models import PROVINCES
    return any((code == c for c, _ in PROVINCES))

def get_user(uid):
    from django.contrib.auth.models import User
    try:
        return User.objects.get(id=uid)
    except User.DoesNotExist:
        return None

def get_track(t):
    return [
        map(float, c.text.split())[:2]
        for c in t.iterchildren()
        if c.tag == '{http://www.google.com/kml/ext/2.2}coord'
    ]

def find_tracks(el):
    tracks = []
    while el is not None:
        if el.tag == '{http://www.google.com/kml/ext/2.2}Track':
            tracks.append(get_track(el))

        elif el.countchildren() > 0:
            tracks += find_tracks(el.getchildren()[0])

        el = el.getnext()
    return tracks

def extract_tracks(f):
    from pykml import parser

    root = parser.fromstring(f.read())
    tracks = find_tracks(root.Document.Placemark)

    return tracks

class Command(BaseCommand):
    help = 'Import KML as a new transportation route'

    option_list = BaseCommand.option_list + (
        make_option('--user-id',
            action='store', type='int', dest='uid',
            help="Submitter's user id"),
        make_option('--province-code',
            action='store', type='string', dest='pid',
            help='Province code'),
        make_option('--city',
            action='store', type='string', dest='city',
            help='City name'),
        make_option('--company',
            action='store', type='string', dest='company',
            help='Transportation company'),
        make_option('--number',
            action='store', type='string', dest='number',
            help='Transportation number'),
        make_option('--origin',
            action='store', type='string', dest='origin',
            help='Origin'),
        make_option('--destination',
            action='store', type='string', dest='destination',
            help='Destination'),
        make_option('--agree-to-contributor-terms',
            action='store_true', dest='agree_to_contributor_terms',
            help='Use this option to agree to the contributor terms'),
        make_option('--merge',
            action='store_true', dest='merge',
            help='Merge with existing transportation'),
        )

    required = ['uid', 'pid', 'city', 'number']

    def handle(self, *args, **kwargs):
        import json

        from ...models import Submission, Transportation
        from ...submission.data import process as processSubmission
        from ... import utils

        if len(args) == 0:
            raise CommandError('A KML file is required')

        for r in self.required:
            if kwargs.get(r) is None:
                raise CommandError('Some of the required options are missing')

        if not kwargs.get('agree_to_contributor_terms', False):
            raise CommandError('Contributor terms agreement is required')

        user = get_user(int(kwargs['uid']))
        if user is None:
            raise CommandError('Invalid user id: {}'.format(kwargs['uid']))

        pid = kwargs['pid']
        if not is_valid_province(pid):
            raise CommandError('Invalid province code: {}'.format(pid))

        # Construct data
        kml = args[0]
        coordinates = extract_tracks(open(kml))
        if len(coordinates) == 0:
            raise CommandError('No track is found')

        city = kwargs['city']
        company = kwargs['company']
        number = kwargs['number']
        data = dict(province=pid,
                    city=city,
                    company=company,
                    number=number,
                    agreeToContributorTerms=True)

        if kwargs.get('origin') is not None:
            data['origin'] = kwargs['origin']
        if kwargs.get('destination') is not None:
            data['destination'] = kwargs['destination']

        geojson = utils.create_geojson_feature(**data)
        geojson['geometry']['coordinates'] = coordinates

        # Check existing transportation
        merge = kwargs.get('merge', False)
        filters = dict(province=pid, city=city, number=number)
        if company is not None:
            filters['company'] = company
        items = Transportation.objects.filter(**filters)
        if not merge and len(items) > 0:
            raise CommandError('Transportation {} in {}, {} already exists. Use --merge to merge the routes.' \
                               .format(number, city, pid))

        parent = None
        source = 'import_transportation_kml'
        if len(items) > 0:
            t = items[0]

            # Merge routes
            if t.submission is not None:
                parent = t.submission
                geojson['geometry']['coordinates'] += t.route.coords
                source = 'import_transportation_kml_merged'

        else:
            t = Transportation(active=False)
            t.province = pid
            t.city = city
            t.company = company
            t.number = number
            if 'origin' in data:
                t.origin = data['origin']
            if 'destination' in data:
                t.destination = data['destination']

        s = Submission()
        s.user = user
        s.raw_geojson = json.dumps(geojson)
        s.source = source
        s.parent = parent
        s.raw_source = open(kml).read()
        processSubmission(s)

        with transaction.commit_on_success():
            s.save()

            t.submission = s
            t.route = s.route
            t.save()

            s.transportation = t
            s.save()

        print 'Transportation is added {} {} - {}, {}. sid={} tid={}'.format(
            company, number, city, pid, s.id, t.id)


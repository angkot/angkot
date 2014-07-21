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

class Command(BaseCommand):
    help = 'Import GeoJSON as a new transportation route'

    option_list = BaseCommand.option_list + (
        make_option('--user-id',
            action='store', type='int', dest='uid',
            help="Submitter's user id"),
        make_option('--agree-to-contributor-terms',
            action='store_true', dest='agree_to_contributor_terms',
            help='Use this option to agree to the contributor terms'),
        make_option('--merge',
            action='store_true', dest='merge',
            help='Merge with existing transportation'),
        )

    required = ['province', 'city', 'number']

    def handle(self, *args, **kwargs):
        import json

        from ...models import Submission, Transportation
        from ...submission.data import process as processSubmission

        if len(args) == 0:
            raise CommandError('A GeoJSON file is required')

        if kwargs.get('uid') is None:
            raise CommandError('User ID is required')

        if not kwargs.get('agree_to_contributor_terms', False):
            raise CommandError('Contributor terms agreement is required')

        user = get_user(int(kwargs['uid']))
        if user is None:
            raise CommandError('Invalid user id: {}'.format(kwargs['uid']))

        geojson = json.load(open(args[0]))

        for f in self.required:
            if geojson['properties'].get(f) is None:
                raise CommandError('Missing property: %s' % f)

        pid = geojson['properties']['province']
        if not is_valid_province(pid):
            raise CommandError('Invalid province code: {}'.format(pid))

        city = geojson['properties']['city']
        number = geojson['properties']['number']
        company = geojson['properties'].get('company')

        merge = kwargs.get('merge', False)
        filters = dict(province=pid, city=city, number=number)
        if company is not None:
            filters['company'] = company
        items = Transportation.objects.filter(**filters)
        if not merge and len(items) > 0:
            raise CommandError('Transportation {} in {}, {} already exists. Use --merge to merge the routes.' \
                               .format(number, city, pid))

        parent = None
        source = 'import_transportation_geojson'
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
            if 'origin' in geojson['properties']:
                t.origin = geojson['properties']['origin']
            if 'destination' in geojson['properties']:
                t.destination = geojson['properties']['destination']

        s = Submission()
        s.user = user
        s.raw_geojson = json.dumps(geojson)
        s.source = source
        s.parent = parent
        processSubmission(s)

        with transaction.commit_on_success():
            s.save()

            t.submission = s
            t.route = s.route
            t.save()

            s.transportation = t
            s.save()

        print('Transportation is added {} {} - {}, {}. sid={} tid={}'.format(
            company, number, city, pid, s.id, t.id))


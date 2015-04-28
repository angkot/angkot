import sys
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Export Route(s) as KML'

    option_list = BaseCommand.option_list + (
        make_option('--all',
            action='store_true', dest='all_routes'),
    )

    def handle(self, *args, **kwargs):
        ids = self._get_ids(args, kwargs.get('all_routes'))
        if len(ids) == 0:
            raise CommandError('Please specify transportation ids or use --all')

        self._export(ids)

    def _get_ids(self, ids, all_routes=False):
        if all_routes:
            return self._get_ids_from_database()
        return ids

    def _get_ids_from_database(self):
        from angkot.route.models import Transportation

        return Transportation.objects.filter(active=True) \
                                     .values_list('pk', flat=True)

    def _export(self, ids):
        from angkot.route.models import Transportation

        from lxml import etree
        from pykml.factory import KML_ElementMaker as KML
        from pykml.factory import ATOM_ElementMaker as ATOM

        def to_placemark(t):
            if t.route is None:
                return None

            geometries = []
            for ls in t.route:
                g = []
                for lon, lat in ls:
                    g.append('{},{}'.format(lon, lat))
                coordinates = ' '.join(g)

                geometry = KML.LineString(
                    KML.coordinates(coordinates))
                geometries.append(geometry)

            name = t.number
            if t.company is not None:
                name = '{} {}'.format(t.company, t.number)

            href = 'https://angkot.web.id/route/#/{}/'.format(t.id)
            return KML.Placemark(
                        KML.name(name),
                        ATOM.link(href=href),
                        ATOM.updated(t.updated.isoformat()),
                        KML.MultiGeometry(*geometries))

        def get_city(t):
            return '{}, {}'.format(t.city, t.get_province_display())

        tt = Transportation.objects.filter(pk__in=ids,
                                           active=True) \
                                   .order_by('province', 'city', 'company', 'number')

        folders = []
        folder = None
        current_city = None
        updated = None
        for t in tt:
            p = to_placemark(t)
            if p is None:
                continue

            city = get_city(t)
            if city != current_city:
                current_city = city
                print('City:', city, file=sys.stderr)

                folder = KML.Folder(
                    KML.name(city))
                folders.append(folder)

            folder.append(p)

            if updated is None or updated < t.updated:
                updated = t.updated

        updated = updated.isoformat()
        description = '''
Public transportation path data by AngkotWebId project.
Copyright © AngkotWebId contributors - https://angkot.web.id

The data is licensed under Open Database License 1.0.
'''.strip()

        kml = KML.kml(KML.Document(
            KML.Name('AngkotWebId'),
            ATOM.author('AngkotWebId Contributors'),
            ATOM.link(href='https://angkot.web.id'),
            ATOM.link(rel='license', href='http://opendatacommons.org/licenses/odbl/1-0/'),
            ATOM.updated(updated),
            KML.description(description),
            *folders))

        print('<?xml version="1.0" encoding="UTF-8"?>')
        print(etree.tostring(kml).decode())



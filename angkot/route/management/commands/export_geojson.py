import sys
import os
import json
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Export Route(s) as GeoJSON'

    option_list = BaseCommand.option_list + (
        make_option('-o', dest='output_directory'),
    )

    def handle(self, *args, **kwargs):
        if len(args) == 0:
            raise CommandError('Please specify transportation id')

        output = kwargs.get('output_directory')

        tid = args[0]
        self._export(tid, output)

    def _export(self, tid, output=None):
        t = self._get_route_or_fail(tid)
        self._write(t, output)

    def _get_route_or_fail(self, tid):
        from angkot.route.models import Transportation

        t = Transportation.objects.filter(pk=tid, active=True)
        if len(t) == 0:
            raise CommandError('Transportation id not found: {}'.format(tid))

        return t[0]

    def _write(self, t, output=None):
        data = t.to_geojson()
        data['properties']['legal'] = dict(
            license='ODbL 1.0',
            copyright='© AngkotWebId Contributors')
        geojson = json.dumps(data, indent=4)

        out = self._get_output(t, output)
        out.write(geojson)
        out.close()

    def _get_output(self, t, output=None):
        if output is None:
            return sys.stdout

        fname = '{} - {} - {} - {} - {}.json'.format(t.id, t.province, t.city, t.company, t.number)
        path = os.path.join(output, fname)
        return open(path, 'w')


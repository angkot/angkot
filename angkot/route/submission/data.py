from datetime import datetime

import geojson
from django.contrib.gis.geos import GEOSGeometry

_max_length = None

def _get_max_lengths(field_map):
    from ..models import Submission
    res = {}

    for field in field_map:
        res[field] = Submission._meta.get_field(field).max_length

    return res

def parseData(submission):
    # Parse
    doc = submission.raw_geojson
    data = geojson.loads(doc, object_hook=geojson.GeoJSON.to_instance)

    # Fill properties
    prop = data.properties
    fields = ['province', 'city', 'company', 'number', 'origin', 'destination']
    for field in fields:
        if field in prop:
            setattr(submission, field, prop[field])
        else:
            setattr(submission, field, None)

    # Fill route
    if len(data.geometry.coordinates):
        submission.route = GEOSGeometry(geojson.dumps(data.geometry))
    else:
        submission.route = None

def validateData(submission):
    # required fields
    fields = ['province', 'city', 'number']
    for field in fields:
        if getattr(submission, field) is None:
            raise ValueError('Incomplete data')

def process(submission):
    try:
        parseData(submission)
        validateData(submission)
        submission.parsed_ok = True
        submission.parsed_error = None
    except Exception as e:
        submission.parsed_error = str(e)
        submission.parsed_ok = False

    submission.parsed_date = datetime.now()

def processAndSave(submission):
    process(submission)
    submission.save()


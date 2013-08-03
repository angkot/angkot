from datetime import datetime

import geojson
from shapely.geometry import asShape

_max_length = None

def _get_max_lengths(field_map):
    from ..models import Submission
    res = {}

    for field in field_map:
        res[field] = Submission._meta.get_field(field).max_length

    return res

def normalize(prop):
    '''Convert old format to the new one'''

    global _max_length

    field_map = dict(city='kota',
                     company='perusahaan',
                     number='nomor',
                     origin='berangkat',
                     destination='jurusan')
    for new, old in field_map.items():
        if old in prop:
            prop[new] = prop[old]

    # Cut values that are too long
    if _max_length is None:
        _max_length = _get_max_lengths(field_map)

    for field in field_map:
        max_length = _max_length[field]
        if field in prop and prop[field] is not None:
            prop[field] = prop[field][:max_length]

    return prop

def parseData(submission):
    # Parse
    doc = submission.raw_geojson
    data = geojson.loads(doc, object_hook=geojson.GeoJSON.to_instance)

    # Fill properties
    prop = normalize(data.properties)
    fields = ['province', 'city', 'company', 'number', 'origin', 'destination']
    for field in fields:
        if field in prop:
            setattr(submission, field, prop[field])
        else:
            setattr(submission, field, None)

    # Fill route
    if len(data.geometry.coordinates):
        geometry = asShape(data.geometry)
        submission.route = geometry.wkt
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
    except StandardError, e:
        submission.parsed_error = str(e)
        submission.parsed_ok = False

    submission.parsed_date = datetime.now()

def processAndSave(submission):
    process(submission)
    submission.save()


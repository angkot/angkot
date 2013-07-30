from datetime import datetime

import geojson
from shapely.geometry import asShape

def normalize(prop):
    '''Convert old format to the new one'''

    field_map = dict(city='kota',
                     company='perusahaan',
                     number='nomor',
                     origin='berangkat',
                     destination='jurusan')
    for new, old in field_map.items():
        if old in prop:
            prop[new] = prop[old]

    return prop

def parseData(submission):
    # Parse
    doc = submission.raw_geojson
    data = geojson.loads(doc, object_hook=geojson.GeoJSON.to_instance)
    geometry = asShape(data.geometry)

    # Fill properties
    prop = normalize(data.properties)
    fields = ['city', 'company', 'number', 'origin', 'destination']
    for field in fields:
        if field in prop:
            setattr(submission, field, prop[field])

    # Fill route
    submission.route = geometry.wkt

def validateData(submission):
    # required fields
    fields = ['city', 'number']
    for field in fields:
        if getattr(submission, field) is None:
            raise ValueError('Incomplete data')

def process(submission):
    parseData(submission)
    try:
        validateData(submission)
        submission.parsed_ok = True
    except ValueError, e:
        submission.parsed_error = str(e)
        submission.parsed_ok = False

    submission.parsed_date = datetime.now()

def processAndSave(submission):
    process(submission)
    submission.save()


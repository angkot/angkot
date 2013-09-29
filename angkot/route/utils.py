def convert_base(num, chars):
    n = len(chars)
    out = []
    while num > 0:
        r = num % n
        num = num // n
        out.append(chars[r])

    return ''.join(out)

def generate_id():
    import random
    import time

    BEGINNING_OF_TIME = 1371079981.267969
    CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' \
            'abcdefghijklmnopqrstuvwxyz' \
            '0123456789'

    rnd = random.randint(0, 9999)
    t = time.time() - BEGINNING_OF_TIME
    t = int(t * 1000)

    return convert_base(t, CHARS)

def to_geojson(obj):
    import geojson
    from shapely.geometry import asMultiLineString

    if obj.route is not None:
        p = asMultiLineString(obj.route)
        geometry = geojson.loads(geojson.dumps(p))
    else:
        geometry = {
            'type': 'MultiLineString',
            'coordinates': []
        }

    return {
        'type': 'Feature',
        'properties': {
            'province': obj.province,
            'city': obj.city,
            'company': obj.company,
            'number': obj.number,
            'origin': obj.origin,
            'destination': obj.destination,
            'accept': [],
        },
        'geometry': geometry
    }

def create_geojson_feature(**kwargs):
    geometry = {
        'type': 'MultiLineString',
        'coordinates': []
    }

    fields = ['province', 'city', 'company', 'number',
              'origin', 'destination']
    properties = {
        'accept': []
    }

    for f in fields:
        if f in kwargs:
            properties[f] = kwargs[f]

    if kwargs.get('agreeToContributorTerms', False):
        properties['accept'].append('ContributorTerms')

    return {
        'type': 'Feature',
        'properties': properties,
        'geometry': geometry
    }


def convert_base(num, chars):
    n = len(chars)
    out = []
    while num > 0:
        r = num % n
        num = num // n
        out.append(chars[r])

    return ''.join(out)

def generate_route_id():
    import random
    import time

    BEGINNING_OF_TIME = 1371079981.267969
    CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' \
            'abcdefghijklmnopqrstuvwxyz' \
            '0123456789'

    rnd = random.randint(0, 9999)
    t = time.time() - BEGINNING_OF_TIME
    t = int(t * 1000)
    print t

    return convert_base(t, CHARS)

def parse_linestring(data):
    import json

    from django.contrib.gis.geos import LineString

    data = json.loads(data)
    if 'type' not in data:
        raise ValueError()
    if 'coordinates' not in data:
        raise ValueError()

    return LineString(data['coordinates'])

def get_coordinates(data):
    if data is None:
        return []
    return [(x, y) for x, y in data]


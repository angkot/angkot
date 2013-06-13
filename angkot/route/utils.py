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

def parse_path(qs):
    numbers = (float(value) for value in qs.split('|'))
    return [(lat, lng) for lat, lng in zip(numbers, numbers)]

def linestring(path):
    from django.contrib.gis.geos import LineString

    return LineString([(lng, lat) for lat, lng in path])


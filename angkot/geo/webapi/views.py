from django.views.decorators.cache import cache_page

from ..models import Province, City

from angkot.common.decorators import wapi

def _province_to_dict(province):
    return dict(pid=province.id,
                name=province.name,
                code=province.code)

def _province_to_pair(province):
    return (province.id, _province_to_dict(province))

def _city_to_dict(city):
    return dict(cid=city.id,
                name=city.name,
                pid=city.province.id)

def _city_to_pair(city):
    return (city.id, _city_to_dict(city))

@cache_page(60 * 60 * 24)
@wapi.endpoint
def province_list(req):
    provinces = Province.objects.filter(enabled=True)
    ordering = [province.id for province in provinces]
    provinces = dict(map(_province_to_pair, provinces))

    last_update = Province.objects.filter(enabled=True) \
                                  .order_by('-updated') \
                                  .values_list('updated', flat=True)[0]

    return dict(provinces=provinces,
                ordering=ordering)

@wapi.endpoint
def city_list(req):
    limit = 500
    try:
        page = int(req.GET.get('page', 0))
    except ValueError:
        page = 0

    start = page * limit
    end = start + limit
    query = City.objects.filter(enabled=True) \
                        .order_by('pk')

    cities = query[start:end]
    cities = dict(map(_city_to_pair, cities))

    total = len(query)

    return dict(cities=cities,
                page=page,
                count=len(cities),
                total=total)


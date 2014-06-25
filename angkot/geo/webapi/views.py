from django.views.decorators.cache import cache_page

from ..models import Province, City

from angkot.common.decorators import wapi

def _to_province(province):
    return dict(id=province.id,
                name=province.name,
                code=province.code)

def _city_to_dict(city):
    data = dict(cid=city.id,
                name=city.name,
                pid=city.province.id)
    return (city.id, data)

@cache_page(60 * 60 * 24)
@wapi.endpoint
def province_list(req):
    provinces = Province.objects.filter(enabled=True)
    provinces = list(map(_to_province, provinces))

    last_update = Province.objects.filter(enabled=True) \
                                  .order_by('-updated') \
                                  .values_list('updated', flat=True)[0]

    return dict(provinces=provinces)

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
    cities = dict(map(_city_to_dict, cities))

    total = len(query)

    return dict(cities=cities,
                page=page,
                count=len(cities),
                total=total)


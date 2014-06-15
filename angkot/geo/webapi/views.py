from django.views.decorators.cache import cache_page

from ..models import Province

from angkot.common.decorators import wapi

def _to_province(province):
    return dict(id=province.id,
                name=province.name,
                code=province.code)

@cache_page(60 * 60 * 24)
@wapi.endpoint
def province_list(req):
    provinces = Province.objects.filter(enabled=True)
    provinces = list(map(_to_province, provinces))

    last_update = Province.objects.filter(enabled=True) \
                                  .order_by('-updated') \
                                  .values_list('updated', flat=True)[0]

    return dict(provinces=provinces)


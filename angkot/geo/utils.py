from .models import Province, City

def get_or_create_city(province, city_name):
    city_name = city_name.strip()
    cities = City.objects.filter(province=province,
                                 name__icontains=city_name)

    for city in cities:
        if city.name.lower() == city_name.lower():
            return city

    city = City(name=city_name,
                province=province)
    city.enabled = True
    city.save()
    return city


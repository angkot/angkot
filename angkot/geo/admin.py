from django.contrib.gis import admin

from angkot.geo.models import Province, City

class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'order', 'pk', 'enabled')

class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'province', 'pk', 'enabled')

admin.site.register(Province, ProvinceAdmin)
admin.site.register(City, CityAdmin)


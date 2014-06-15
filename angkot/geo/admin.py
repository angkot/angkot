from django.contrib.gis import admin

from .models import Province

class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'pk', 'enabled')

admin.site.register(Province, ProvinceAdmin)


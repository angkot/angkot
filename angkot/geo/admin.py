from django.contrib.gis import admin

from .models import Province

class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'pk')

admin.site.register(Province, ProvinceAdmin)


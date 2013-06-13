from django.contrib.gis import admin

from .models import Route

admin.site.register(Route, admin.GeoModelAdmin)


from django.contrib.gis import admin

import reversion

from .models import Author, Line, Route

class BaseAuthoredAdmin(reversion.VersionAdmin, admin.ModelAdmin):
    readonly_fields = ('author',)

    def save_model(self, request, obj, form, change):
        obj.author = Author.objects.create_from_request(request)
        obj.save()

class LineAdmin(BaseAuthoredAdmin):
    pass

class RouteAdmin(BaseAuthoredAdmin):
    pass

admin.site.register(Line, LineAdmin)
admin.site.register(Route, RouteAdmin)


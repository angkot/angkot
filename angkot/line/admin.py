from django.contrib.gis import admin
from django.contrib.postgres.fields import ArrayField
from django.core.urlresolvers import reverse
from django.utils.html import escape
from django.utils.safestring import mark_safe

import reversion

from angkot.line.models import Line, Route
from angkot.account.admin import BaseAuthoredAdmin

class LineAdmin(reversion.VersionAdmin, BaseAuthoredAdmin):
    list_display = ('number', 'type',
                    'enabled',
                    'name', 'mode', 'city',
                    'updated', 'author_link', 'id')

    fieldsets = (
        (None, {
            'fields': ('type', 'number', 'name', 'mode', 'enabled'),
        }),
        ('Location', {
            'fields': ('city',),
        }),
        (None, {
            'fields': ('info',)
        }),
        ('Meta', {
            'fields': ('author_link', 'updated', 'created')
        }),
    )

class RouteAdmin(reversion.VersionAdmin, BaseAuthoredAdmin):
    def locations_list(obj):
        if obj.locations is None:
            return ''

        if len(obj.locations) > 5:
            locations = list(map(escape, obj.locations[:2])) \
                        + ['&hellip;'] \
                        + list(map(escape, obj.locations[-2:]))
        else:
            locations = list(map(escape, obj.locations[:5]))
        return mark_safe(' &rarr; '.join(locations))

    def has_path(obj):
        return obj.path is not None
    has_path.boolean = True

    list_display = ('line', 'name', 'enabled', has_path, locations_list,
                    'ordering', 'author_link', 'id')

    readonly_fields = BaseAuthoredAdmin.readonly_fields + ('line_link',)

    fieldsets = (
        (None, {
            'fields': ('line', 'line_link', 'name', 'locations', 'ordering', 'enabled'),
        }),
        ('Path', {
            'fields': ('path',),
        }),
        ('Meta', {
            'fields': ('author_link', 'updated', 'created')
        }),
    )

    formfield_overrides = {
        ArrayField: {'widget': admin.widgets.Textarea}
    }

    def line_link(self, obj):
        if obj.line is None:
            return None

        url = reverse('admin:line_line_change', args=(obj.line.id,))
        return mark_safe('<a href="{}">{}</a>'.format(url, obj.line))
    line_link.short_description = 'Line'

    def save_model(self, request, obj, form, change):
        if obj.locations is not None:
            obj.locations = list(map(lambda x: x.strip(), obj.locations))

        super(RouteAdmin, self).save_model(request, obj, form, change)

admin.site.register(Line, LineAdmin)
admin.site.register(Route, RouteAdmin)


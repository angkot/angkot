from django.contrib.gis import admin
from django.core.urlresolvers import reverse
from django.utils.html import escape
from django.utils.safestring import mark_safe

import reversion
from djorm_pgarray.fields import ArrayField

from .models import Author, Line, Route

class AuthorAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'ip_address', 'user_agent', 'referer',
                       'created')

    list_display = ('user', 'ip_address', 'created', 'referer', 'user_agent')

class BaseAuthoredAdmin(reversion.VersionAdmin, admin.ModelAdmin):
    readonly_fields = ('author_link', 'created', 'updated')

    def save_model(self, request, obj, form, change):
        obj.author = Author.objects.create_from_request(request)
        obj.save()

    def author_link(self, obj):
        if obj.author is None:
            return None

        url = reverse('admin:line_author_change', args=(obj.author.id,))
        return mark_safe('<a href="{}">{}</a>'.format(url, obj.author))

    author_link.short_description = 'Author'

class LineAdmin(BaseAuthoredAdmin):
    list_display = ('label', 'enabled', 'name', 'mode', 'province', 'city',
                    'updated', 'author_link', 'id')

    fieldsets = (
        (None, {
            'fields': ('label', 'name', 'mode', 'enabled'),
        }),
        ('Location', {
            'fields': ('province', 'city'),
        }),
        (None, {
            'fields': ('info',)
        }),
        ('Meta', {
            'fields': ('author_link', 'updated', 'created')
        }),
    )

class RouteAdmin(BaseAuthoredAdmin):
    def locations_list(obj):
        if obj.locations is None:
            return ''

        locations = list(map(escape, obj.locations[:5]))
        if len(obj.locations) > 5:
            locations.append('&hellip;')
        return mark_safe(' &rarr; '.join(locations))

    def has_path(obj):
        return obj.path is not None
    has_path.boolean = True

    list_display = ('line', 'name', 'enabled', has_path, locations_list,
                    'ordering', 'author_link', 'id')

    readonly_fields = BaseAuthoredAdmin.readonly_fields + ('line_link',)

    fieldsets = (
        (None, {
            'fields': ('line_link', 'name', 'locations', 'ordering', 'enabled'),
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

admin.site.register(Author, AuthorAdmin)
admin.site.register(Line, LineAdmin)
admin.site.register(Route, RouteAdmin)


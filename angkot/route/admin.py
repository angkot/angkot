from django.contrib.gis import admin

from .models import Transportation, Submission

class TransportationAdmin(admin.GeoModelAdmin):
    list_display = ('province', 'city', 'company', 'number', 'origin',
                    'destination', 'active', 'updated')

class SubmissionAdmin(admin.GeoModelAdmin):
    def visitor_id(obj):
        return '<span title="{}">{}</span>'.format(obj.visitor_id, str(obj.visitor_id)[0:8])
    visitor_id.allow_tags = True
    visitor_id.admin_order_field = 'visitor_id'

    list_display = ('submission_id', 'ip_address', visitor_id, 'parsed_ok', 'created',)

admin.site.register(Transportation, TransportationAdmin)
admin.site.register(Submission, SubmissionAdmin)


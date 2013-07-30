from django.contrib.gis import admin

from .models import Submission

class SubmissionAdmin(admin.GeoModelAdmin):
    def visitor_id(obj):
        return '<span title="{}">{}</span>'.format(obj.visitor_id, str(obj.visitor_id)[0:8])
    visitor_id.allow_tags = True
    visitor_id.admin_order_field = 'visitor_id'

    list_display = ('submission_id', 'ip_address', visitor_id, 'parsed_ok', 'created',)

admin.site.register(Submission, SubmissionAdmin)


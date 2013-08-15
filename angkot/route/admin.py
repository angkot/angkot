from django.contrib.gis import admin

from .models import Transportation, Submission

class TransportationAdmin(admin.GeoModelAdmin):
    list_display = ('province', 'city', 'company', 'number', 'origin',
                    'destination', 'active', 'updated')

class SubmissionAdmin(admin.GeoModelAdmin):
    list_display = ('submission_id', 'ip_address', 'parsed_ok',
                    'created', 'province', 'city', 'company', 'number')

admin.site.register(Transportation, TransportationAdmin)
admin.site.register(Submission, SubmissionAdmin)


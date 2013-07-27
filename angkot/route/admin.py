from django.contrib.gis import admin

from .models import Submission

class SubmissionAdmin(admin.GeoModelAdmin):
    list_display = ('submission_id', 'ip_address', 'created',)

admin.site.register(Submission, SubmissionAdmin)


from django.contrib.gis import admin

from .models import Transportation, Submission

class TransportationAdmin(admin.GeoModelAdmin):
    list_display = ('province', 'city', 'company', 'number', 'origin',
                    'destination', 'active', 'updated')

class SubmissionAdmin(admin.GeoModelAdmin):
    def user(obj):
        if obj.user is None:
            return '(none)'
        if obj.user.email is not None:
            return '{} - {}'.format(obj.user.first_name, obj.user.email)
        return obj.user.first_name

    list_display = ('submission_id', 'ip_address', user, 'parsed_ok',
                    'created', 'province', 'city', 'company', 'number')

admin.site.register(Transportation, TransportationAdmin)
admin.site.register(Submission, SubmissionAdmin)


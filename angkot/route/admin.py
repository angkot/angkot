from django.contrib.gis import admin

from .models import Transportation, Submission

class TransportationAdmin(admin.GeoModelAdmin):
    def updater(obj):
        if obj.submission is None:
            return '(unknown)'
        user = obj.submission.user
        if user is None:
            return '(unknown)'
        if user.email is not None:
            return '{} - {}'.format(user.first_name, user.email)
        return user.first_name

    def submission(obj):
        s = obj.submission
        if s is None:
            return '(unknown)'
        return '<a href="../submission/{}/">{}</a>'.format(s.id, s.submission_id)
    submission.allow_tags = True

    list_display = ('province', 'city', 'company', 'number', 'origin',
                    'destination', 'active', 'updated', submission, updater)

    def save_model(self, request, obj, form, change):
        obj.save_as_new_submission(request, 'admin_page')

class SubmissionAdmin(admin.GeoModelAdmin):
    def user(obj):
        if obj.user is None:
            return '(none)'
        if obj.user.email is not None:
            return '{} - {}'.format(obj.user.first_name, obj.user.email)
        return obj.user.first_name

    def parent(obj):
        if obj.parent is not None:
            return obj.parent.submission_id

    list_display = ('submission_id', 'ip_address', user, 'parsed_ok', 'source', parent,
                    'created', 'province', 'city', 'company', 'number')

admin.site.register(Transportation, TransportationAdmin)
admin.site.register(Submission, SubmissionAdmin)


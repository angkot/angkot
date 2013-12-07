from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    args = '<submission-text-id>'
    help = 'Parse submitted route'

    option_list = BaseCommand.option_list + (
        make_option('--dry-run',
            action='store_true',
            dest='dry-run',
            default=False,
            help="Only parse and validate, don't save"),
        )

    def handle(self, *args, **options):
        from ...submission import data
        from ...models import Submission

        if len(args) < 1:
            raise CommandError('Please specify submission id')

        sid = args[0]

        try:
            submission = Submission.objects.get(submission_id=sid)
        except Submission.DoesNotExist:
            raise CommandError('Submission id is not found: {}'.format(sid))

        try:
            data.process(submission)
            print('Parsing    OK')

            fields = ['city', 'company', 'number', 'origin', 'destination']
            for field in fields:
                print('- {:12}: {}'.format(field, getattr(submission, field)))

        except Exception as e:
            raise CommandError('Unable to parse submission: {}'.format(e))

        if submission.parsed_ok:
            print('Validation OK')
        else:
            print('Validation FAIL')

        if options['dry-run']:
            print('Submission NOT updated: dry-run mode')
        else:
            submission.save()
            print('Submission UPDATED')


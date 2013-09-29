from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Update city and company name capitalization'

    option_list = BaseCommand.option_list + (
        make_option('--update',
            action='store_true', dest='update'),
    )

    def handle(self, *args, **kwargs):
        import string

        from ...models import Transportation

        update = kwargs['update']
        if not update:
            print 'Running in preview mode. Use --update to apply changes'

        for t in Transportation.objects.all():
            ci = string.capwords(t.city)
            co = None
            if t.company is not None:
                co = string.capwords(t.company)

            if ci != t.city or co != t.company:
                if update:
                    t.city = ci
                    t.company = co
                    t.save()
                print '-', t


from django.contrib import admin
from django.core.urlresolvers import reverse

from .models import Author

class AuthorAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'ip_address', 'user_agent', 'referer',
                       'created')

    list_display = ('user', 'ip_address', 'created', 'referer', 'user_agent')

class BaseAuthoredAdmin(admin.ModelAdmin):
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

admin.site.register(Author, AuthorAdmin)


from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.template import RequestContext

from angkot.decorators import login_required

@login_required
def index(request):
    return render_to_response('account/index.html',
                              context_instance=RequestContext(request))

def login_page(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('account_index'))
    return render_to_response('account/login.html',
                              context_instance=RequestContext(request))

def logout_page(request):
    from django.contrib.auth import logout

    logout(request)
    return render_to_response('account/logout.html',
                              context_instance=RequestContext(request))


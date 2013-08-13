from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.template import RequestContext

from angkot.decorators import api, login_required

@login_required
def index(request):
    return render_to_response('account/index.html',
                              context_instance=RequestContext(request))

def login_page(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('account_index'))
    return render_to_response('account/login.html',
                              context_instance=RequestContext(request))

@login_required
def login_success(request):
    return render_to_response('account/login_success.html',
                              context_instance=RequestContext(request))

def logout_page(request):
    from django.contrib.auth import logout

    logout(request)
    return render_to_response('account/logout.html',
                              context_instance=RequestContext(request))

@api
def account_info(request):
    res = {'authenticated': request.user.is_authenticated()}
    if request.user.is_authenticated():
        res['username'] = request.user.username
        res['first_name'] = request.user.first_name
        res['last_name'] = request.user.last_name

    return res


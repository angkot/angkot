from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import requires_csrf_token, ensure_csrf_cookie

from .utils import generate_route_id
from .decorators import api

def index(request):
    route_id = generate_route_id()
    return redirect('route_editor', route_id=route_id)

@ensure_csrf_cookie
def editor(request, route_id):
    return render_to_response('route/editor.html',
                              context_instance=RequestContext(request))

@requires_csrf_token
@api
def submit(request, route_id):
    return {}


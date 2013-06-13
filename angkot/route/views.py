from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import requires_csrf_token, ensure_csrf_cookie

from angkot.decorators import api
from .decorators import requires_route_id
from .models import Route

def index(request):
    route = Route()
    route.save()

    route_id = route.route_id
    return redirect('route_editor', route_id=route_id)

@ensure_csrf_cookie
@requires_route_id
def editor(request, route):
    return render_to_response('route/editor.html',
                              context_instance=RequestContext(request))

@requires_csrf_token
@api
def submit(request, route_id):
    return {}


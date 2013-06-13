from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import requires_csrf_token, ensure_csrf_cookie

from angkot.decorators import api
from .utils import parse_linestring, get_coordinates
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
@requires_route_id
@api
def submit(request, route):
    try:
        path = parse_linestring(request.POST.get('data', None))
    except ValueError:
        return False, 401, dict(code=401, msg="bad coordinates")

    name = request.POST.get('name', None)
    if name is None:
        return False, 401, dict(code=401, msg="name is required")

    route.transportation_name = name
    route.origin = request.POST.get('origin', None)
    route.destination = request.POST.get('destination', None)
    route.vehicle_type = request.POST.get('type', None)
    route.path = path
    route.save()


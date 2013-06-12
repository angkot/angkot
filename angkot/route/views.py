from django.shortcuts import redirect, render_to_response
from django.template import RequestContext

from .utils import generate_route_id

def index(request):
    route_id = generate_route_id()
    return redirect('route_editor', route_id=route_id)

def editor(request, route_id):
    return render_to_response('route/editor.html',
                              context_instance=RequestContext(request))


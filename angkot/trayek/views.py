from django.shortcuts import render_to_response
from django.template import RequestContext

def index(request):
    print 'Method:', request.method
    if request.method == 'POST':
        print '- post data:', request.POST
        print '- geojson:', request.POST['geojson']
    return render_to_response('trayek/trayek.html',
                              context_instance=RequestContext(request))


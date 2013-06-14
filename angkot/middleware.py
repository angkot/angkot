class VisitorMiddleware(object):
    def process_request(self, request):
        if 'visitor-id' not in request.session:
            import uuid
            request.session['visitor-id'] = uuid.uuid4()
        request.visitor_id = request.session['visitor-id']


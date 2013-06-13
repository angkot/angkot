def requires_route_id(func):
    from .models import Route

    def _func(request, route_id, *args, **kwargs):
        route = Route.objects.get(route_id=route_id)
        return func(request, route, *args, **kwargs)

    return _func


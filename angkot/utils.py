def log_extra(request):
    return dict(user=request.user,
                uid=request.user.id)


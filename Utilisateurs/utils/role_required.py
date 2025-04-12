from django.http import HttpResponseForbidden

def role_required(allowed_roles=[]):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return HttpResponseForbidden("Connexion requise.")
            user_role = request.user.get_role()
            if user_role in allowed_roles:
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("Accès interdit.")
        return wrapper
    return decorator

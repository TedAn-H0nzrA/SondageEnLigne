from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.contrib import messages

def role_required(allowed_roles):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            
            user_role = request.user.get_role()
            print(f"Checking role: {user_role} against allowed roles: {allowed_roles}")  # Debug
            
            if user_role not in allowed_roles:
                messages.error(request, "Vous n'avez pas les permissions nécessaires.")
                if user_role == 'admin':
                    return redirect('admin_dashboard')
                elif user_role == 'enqueteur':
                    return redirect('enqueteur_dashboard')
                return redirect('login')
                
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

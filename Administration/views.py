from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from Utilisateurs.models import Utilisateurs, User_role
from Enquetes.models import Enquete
from Responses.models import Responses
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from Utilisateurs.forms import RegisterForm
from django.contrib.auth.hashers import make_password

@staff_member_required
def dashboard(request):
    context = {
        'total_users': Utilisateurs.objects.count(),
        'total_surveys': Enquete.objects.count(),
        'total_responses': Responses.objects.count(),
        'active': 'dashboard'
    }
    return render(request, 'Auth/admin_dashboard.html', context)

@staff_member_required
def manage_users(request):
    # Remove select_related since the relationship might be through RoleUserMapping
    users = Utilisateurs.objects.all()
    return render(request, 'Admin/dashboard/users.html', {
        'users': users,
        'active': 'users'
    })

@staff_member_required
def statistics(request):
    stats = {
        'active_users': Utilisateurs.objects.filter(is_active=True).count(),
        'active_surveys': Enquete.objects.filter(status='actif').count(),
        'total_responses': Responses.objects.count()
    }
    return render(request, 'Admin/dashboard/stats.html', {
        'stats': stats,
        'active': 'stats'
    })

@staff_member_required
def data_explorer(request):
    data_type = request.GET.get('type', 'surveys')
    if data_type == 'surveys':
        data = Enquete.objects.all()
    elif data_type == 'responses':
        data = Responses.objects.all()
    else:
        data = Utilisateurs.objects.all()
    
    return render(request, 'Admin/dashboard/data.html', {
        'data': data,
        'data_type': data_type,
        'active': 'data'
    })

@staff_member_required
def add_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            role_name = request.POST.get('role')
            try:
                role = User_role.objects.get(roleName=role_name)
                user.user_role = role
                user.save()
                messages.success(request, "Utilisateur créé avec succès")
                return redirect('admin_dashboard:users')
            except User_role.DoesNotExist:
                messages.error(request, "Le rôle spécifié n'existe pas")
    else:
        form = RegisterForm()
    
    roles = User_role.objects.all()
    return render(request, 'Admin/dashboard/users.html', {
        'form': form,
        'roles': roles,
        'active': 'users'
    })

@staff_member_required
def edit_user(request, user_id):
    user = get_object_or_404(Utilisateurs, id=user_id)
    if request.method == 'POST':
        form = RegisterForm(request.POST, instance=user)
        if form.is_valid():
            try:
                # Get the selected role
                role_name = request.POST.get('role')
                role = User_role.objects.get(roleName=role_name)
                
                # Update user
                user = form.save(commit=False)
                user.user_role = role
                user.save()
                
                messages.success(request, "Utilisateur modifié avec succès")
                return redirect('admin_dashboard:users')
            except User_role.DoesNotExist:
                messages.error(request, "Le rôle sélectionné n'existe pas")
    else:
        form = RegisterForm(instance=user)
    
    roles = User_role.objects.all()
    return render(request, 'Admin/dashboard/edit_user.html', {
        'form': form,
        'roles': roles,
        'user': user,
        'active': 'users'
    })

@staff_member_required
def delete_user(request, user_id):
    user = get_object_or_404(Utilisateurs, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, "Utilisateur supprimé avec succès")
        return redirect('admin_dashboard:users')
    
    return render(request, 'Admin/dashboard/delete_user.html', {
        'user': user,
        'active': 'users'
    })

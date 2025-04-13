from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from .forms import RegisterForm, LoginForm
from .models import Utilisateurs, RoleUserMapping, User_role
from django.contrib.auth.decorators import login_required
from .utils.role_required import role_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from Enquetes.models import Enquete
from Responses.models import Responses

# Inscription
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                # Récupérer le rôle enquêteur
                role = User_role.objects.get(roleName="enqueteur")
                
                # Créer l'utilisateur
                user = form.save(commit=False)
                user.save()
                
                # Assigner le rôle
                RoleUserMapping.objects.create(userID=user, user_roleID=role)
                
                # Connecter l'utilisateur
                login(request, user)
                return redirect('enqueteur_dashboard')
                
            except User_role.DoesNotExist:
                form.add_error(None, "Erreur système: rôle non trouvé")
    else:
        form = RegisterForm()
    return render(request, 'Auth/register.html', {"form": form})



# Connexion
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = Utilisateurs.objects.filter(email=email).first()
            
            if user and user.check_password(password):
                login(request, user)
                user_role = user.get_role()
                
                # Ajout de debug pour vérifier le rôle
                print(f"User role: {user_role}")  # Debug
                
                if user_role == 'admin':
                    print("Redirecting to admin dashboard")  # Debug
                    return redirect('admin_dashboard')
                elif user_role == 'enqueteur':
                    print("Redirecting to enqueteur dashboard")  # Debug
                    return redirect('enqueteur_dashboard')
                else:
                    print(f"Unknown role: {user_role}")  # Debug
                    return redirect('login')
            else:
                form.add_error(None, "Identifiant ou mot de passe incorrect.")
    else:
        form = LoginForm()
    return render(request, "Auth/login.html", {"form": form})


# Déconnexion
def logout_views(request):
    logout(request)
    return redirect("login")

@login_required
@role_required(['admin'])
def admin_dashboard(request):
    return render(request, "Auth/admin_dashboard.html")

@login_required
@role_required(['enqueteur'])
def enqueteur_dashboard(request):
    return render(request, "Auth/enqueteur_dashboard.html")

@staff_member_required
def admin_users(request):
    users = Utilisateurs.objects.all().select_related('user_role')
    roles = User_role.objects.all()
    
    return render(request, 'Admin/dashboard/users.html', {
        'users': users,
        'roles': roles,
        'active': 'users'
    })

@staff_member_required
def admin_stats(request):
    today = timezone.now()
    week_ago = today - timedelta(days=7)
    
    stats = {
        'total_users': Utilisateurs.objects.count(),
        'enqueteurs_count': Utilisateurs.objects.filter(user_role__roleName='enqueteur').count(),
        'active_users': Utilisateurs.objects.filter(is_active=True).count(),
        'total_surveys': Enquete.objects.count(),
        'active_surveys': Enquete.objects.filter(status='actif').count(),
        'completed_surveys': Enquete.objects.filter(status='complete').count(),
        'total_responses': Responses.objects.count(),
        'today_responses': Responses.objects.filter(responseDatetime__date=today.date()).count(),
        'week_responses': Responses.objects.filter(responseDatetime__gte=week_ago).count(),
    }
    
    return render(request, 'Admin/dashboard/stats.html', {
        'stats': stats,
        'active': 'stats'
    })

@staff_member_required
def admin_data(request):
    data_type = request.GET.get('type', 'surveys')
    page = request.GET.get('page', 1)
    
    if data_type == 'surveys':
        queryset = Enquete.objects.all()
    elif data_type == 'responses':
        queryset = Responses.objects.all()
    else:
        queryset = Utilisateurs.objects.all()
    
    paginator = Paginator(queryset, 25)
    data = paginator.get_page(page)
    
    return render(request, 'Admin/dashboard/data.html', {
        'data': data,
        'active': 'data'
    })
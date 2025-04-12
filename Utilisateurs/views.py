from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, LoginForm
from .models import Utilisateurs, RoleUserMapping, User_role
from django.contrib.auth.decorators import login_required
from .utils.role_required import role_required

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
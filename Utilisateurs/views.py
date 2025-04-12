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
            role = User_role.objects.get(roleName = "enqueteur")
            user = form.save(commit=False)
            user.save()
            RoleUserMapping.objects.create(userID=user, user_roleID=role)
            login(request, user)

            if role.roleName == 'admin':
                return redirect('admin_dashboard')
            elif role.roleName == 'enqueteur':
                return redirect('enqueteur_dashboard')
            return redirect("accueil")
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
                if user_role == 'admin':
                    return redirect("admin_dashboard")
                elif user_role == 'enqueteur':
                    return redirect("enqueteur_dashboard")
                else:
                    # Redirection par défaut
                    return redirect("accueil_enqueteur")
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
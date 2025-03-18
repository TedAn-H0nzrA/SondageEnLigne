from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, LoginForm
from .models import Utilisateurs


# Vue pour l'inscription
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save() # Enregistrement de l'utilisateur
            return redirect("accueil") # Redirection vers la page d'accueil
    else:
        form = RegisterForm()

    return render(request, 'Auth/register.html', {"form": form})



def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            # Verification si l'utilisateur existe via email
            user = Utilisateurs.objects.filter(email = email).first()

            # Verification du mot de passe
            if user and user.check_password(password):
                login(request, user)
                return redirect("accueil")
            else:
                form.add_error(None, "Identifiant ou mot de passe incorrect.") # Message d'erreur si identifiant ou mdp incorrecte
        
    else:
        form = LoginForm()
            
    return render(request, "Auth/login.html", {"form" : form})


# Vue pour la deconnexion
def logout_views(request):
    logout(request)
    return redirect("login")
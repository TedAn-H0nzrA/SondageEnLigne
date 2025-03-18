from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

# Récupération du modél utilisateus personnalisé
User = get_user_model()

# Class connexion / Formulaire de connexion
class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget = forms.PasswordInput)
    
# Class création d'utilisateur / Formulaire d'inscription
class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username", "password1", "password2"]

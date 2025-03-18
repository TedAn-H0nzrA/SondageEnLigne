from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def welcome(request):
    return render(request, 'Core/welcome.html')

@login_required
def accueil(request):
    return render(request, 'Core/accueil.html')
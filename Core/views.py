from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from Enquetes.models import Enquete

def welcome(request):
    return render(request, 'Core/welcome.html')

def accueil(request):
    return render(request, 'Core/accueil.html')

def home_participant(request):
    sondages_actifs = Enquete.objects.filter(status='actif')
    return render(request, 'Core/home_participant.html', {
        'sondages': sondages_actifs
    })

def home_user(request):
    return render(request, 'Core/home_user.html')
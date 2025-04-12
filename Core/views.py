from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from Enquetes.models import Enquete

def welcome(request):
    return render(request, 'Core/welcome.html')

@login_required
def accueil(request):
    # Récupérer uniquement les sondages actifs
    sondages_actifs = Enquete.objects.filter(status='actif')
    return render(request, 'Core/accueil.html', {
        'sondages': sondages_actifs
    })
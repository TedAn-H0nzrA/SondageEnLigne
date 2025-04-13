from django.urls import path
from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('participant/', views.home_participant, name='home_participant'),
    path('user/', views.home_user, name='home_user'),
]
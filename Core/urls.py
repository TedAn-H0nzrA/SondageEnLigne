from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name = 'welcome'),
    path('accueil-enqueteur/', views.accueil, name = 'accueil_enqueteur'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name = 'login'),
    path('register/', views.register_view,name = 'register'),
    path('logout/', views.logout_views, name = 'logout'),

     # Dashboards
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('enqueteur-dashboard/', views.enqueteur_dashboard, name='enqueteur_dashboard'),
]
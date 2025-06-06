"""
URL configuration for SondageEnLigne project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('django-admin/', admin.site.urls),  # Changed to avoid conflict
    path('', include('Core.urls')),
    path('user/', include('Utilisateurs.urls')),
    path('enquetes/', include('Enquetes.urls')),
    path('responses/', include('Responses.urls', namespace='responses')),
    path('admin/', include('Administration.urls', namespace='admin_dashboard')),
]

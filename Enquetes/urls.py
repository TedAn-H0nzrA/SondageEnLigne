from django.urls import path
from .views import enquete_list, enquete_detail, enquete_create, enquete_update, enquete_delete, enquete_response_create, question_create

urlpatterns = [
    # Enquêtes
    path('', enquete_list, name='enquete_list'),
    path('new/', enquete_create, name='enquete_create'),
    path('<int:pk>/', enquete_detail, name='enquete_detail'),
    path('<int:pk>/edit/', enquete_update, name='enquete_update'),
    path('<int:pk>/delete/', enquete_delete, name='enquete_delete'),

    # Réponses aux enquêtes
    path('<int:pk>/respond/', enquete_response_create, name='enquete_respond'),

    # Questions
    path('<int:enquete_id>/add-question/', question_create, name='question_create'),
]

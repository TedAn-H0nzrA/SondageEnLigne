from django.urls import path
from . import views

app_name = 'responses'

urlpatterns = [
    path('participer/<int:enquete_id>/', views.participer_sondage, name='participer_sondage'),
    path('submit/<int:enquete_response_id>/<int:question_id>/', views.submit_response, name='submit_response'),
    path('success/', views.success_page, name='success_page'),
]

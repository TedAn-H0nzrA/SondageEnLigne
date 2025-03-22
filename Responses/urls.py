from django.urls import path
from .views import submit_response, success_page

urlpatterns = [
    path('submit/<int:enquete_response_id>/<int:question_id>/', submit_response, name='submit_response'),
    path('success/', success_page, name = 'success_page'),
]

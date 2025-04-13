from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.utils import timezone
from .models import Responses, EnqueteResponse, Question, ResponseSelection
from .forms import ResponseForm, ParticipationForm
from Enquetes.models import Enquete
import uuid

def submit_response(request, enquete_response_id, question_id):
    enquete_response = get_object_or_404(EnqueteResponse, id=enquete_response_id)
    question = get_object_or_404(Question, id=question_id)
    
    # Debug print - Changed questionType to responseType
    print(f"Question type: {question.responseType}")
    print(f"Available options: {ResponseSelection.objects.filter(questionID=question)}")
    
    # Vérifier si la question a déjà été répondue
    if Responses.objects.filter(enqueteResponsesID=enquete_response, questionID=question).exists():
        messages.error(request, "Vous avez déjà répondu à cette question.")
        return redirect('responses:question_list', enquete_response_id=enquete_response_id)
    
    if request.method == 'POST':
        form = ResponseForm(question, request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.enqueteResponsesID = enquete_response
            response.questionID = question
            response.save()
            
            # Confirmer l'email après la première réponse
            if not enquete_response.is_email_confirmed:
                enquete_response.confirm_email()
            
            # Trouver la prochaine question non répondue
            next_question = Question.objects.filter(
                enqueteID=enquete_response.enqueteID,
                id__gt=question_id
            ).exclude(
                responses__enqueteResponsesID=enquete_response
            ).first()
            
            if next_question:
                return redirect('responses:submit_response', 
                             enquete_response_id=enquete_response_id,
                             question_id=next_question.id)
            else:
                enquete_response.status = 'complete'
                enquete_response.validationDatetime = timezone.now()
                enquete_response.save()
                return redirect('responses:success_page')
    else:
        form = ResponseForm(question)
    
    return render(request, 'Responses/submit_response.html', {
        'form': form,
        'question': question,
        'enquete': enquete_response.enqueteID,
        'questions_remaining': Question.objects.filter(enqueteID=enquete_response.enqueteID).exclude(
            responses__enqueteResponsesID=enquete_response
        ).count()
    })

def success_page(request):
    return render(request, 'Responses/success_page.html')

def participer_sondage(request, enquete_id):
    enquete = get_object_or_404(Enquete, id=enquete_id, status='actif')
    
    if request.method == 'POST':
        form = ParticipationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            
            # Vérifier si l'email a déjà participé
            existing_response = EnqueteResponse.objects.filter(
                enqueteID=enquete,
                email=email,
                is_email_confirmed=True
            ).exists()
            
            if existing_response:
                messages.error(request, "Vous avez déjà participé à ce sondage.")
                return redirect('accueil')
            
            participation = EnqueteResponse.objects.create(
                enqueteID=enquete,
                email=email,
                token=str(uuid.uuid4())[:30]
            )
            
            # Rediriger vers la première question
            questions = Question.objects.filter(enqueteID=enquete)
            if questions.exists():
                return redirect('responses:submit_response', 
                             enquete_response_id=participation.id,
                             question_id=questions.first().id)
            else:
                messages.warning(request, "Ce sondage ne contient pas encore de questions.")
                return redirect('accueil')
    else:
        form = ParticipationForm()

    return render(request, 'Responses/participer.html', {
        'form': form,
        'enquete': enquete
    })
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Enquete, EnqueteResponse, Question
from .forms import EnqueteForm, EnqueteResponseForm, QuestionForm
from Utilisateurs.utils.role_required import role_required

# Liste des enquêtes
@login_required
def enquete_list(request):
    # Si l'utilisateur est admin, il voit tout
    if request.user.get_role() == 'admin':
        enquetes = Enquete.objects.all()
    else:
        # Sinon il ne voit que ses enquêtes
        enquetes = Enquete.objects.filter(userID=request.user)
    return render(request, 'Enquetes/list.html', {'enquetes': enquetes})

# Détails d'une enquête
@login_required
@role_required(['admin', 'enqueteur'])
def enquete_detail(request, pk):
    # Si l'utilisateur est admin, il peut voir toutes les enquêtes
    if request.user.get_role() == 'admin':
        enquete = get_object_or_404(Enquete, id=pk)
    else:
        # Sinon il ne peut voir que ses enquêtes
        enquete = get_object_or_404(Enquete, id=pk, userID=request.user)
        
    questions = Question.objects.filter(enqueteID=enquete)
    return render(request, 'Enquetes/detail.html', {
        'enquete': enquete, 
        'questions': questions
    })

# Création d'une enquête
@login_required
def enquete_create(request):
    if request.method == 'POST':
        form = EnqueteForm(request.POST)
        if form.is_valid():
            enquete = form.save(commit=False)
            enquete.userID = request.user
            enquete.save()
            return redirect('enquete_list')
    else:
        form = EnqueteForm()
    return render(request, 'Enquetes/forme.html', {'form': form})

# Modification d'une enquête
@login_required
def enquete_update(request, pk):
    enquete = get_object_or_404(Enquete, id=pk)
    if request.method == 'POST':
        form = EnqueteForm(request.POST, instance=enquete)
        if form.is_valid():
            form.save()
            return redirect('enquete_detail', pk=enquete.id)
    else:
        form = EnqueteForm(instance=enquete)
    return render(request, 'Enquetes/forme.html', {'form': form})

# Suppression d'une enquête
@login_required
def enquete_delete(request, pk):
    enquete = get_object_or_404(Enquete, id = pk)
    if request.method == 'POST':
        enquete.delete()
        return redirect('enquete_list')
    return render(request, 'Enquetes/confirm_delete.html', {'enquete': enquete})

# Création d'une réponse à une enquête
def enquete_response_create(request, pk):
    enquete = get_object_or_404(Enquete, id=pk)
    if request.method == 'POST':
        form = EnqueteResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.enqueteID = enquete
            response.save()
            return redirect('enquete_detail', pk=enquete.id)
    else:
        form = EnqueteResponseForm()
    return render(request, 'Enquetes/response_form.html', {'form': form})

# Création d'une question pour une enquête
@login_required
def question_create(request, pk):
    enquete = get_object_or_404(Enquete, id=pk)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.enqueteID = enquete
            question.save()
            return redirect('enquete_detail', pk=enquete.id)
    else:
        form = QuestionForm()
    return render(request, 'Enquetes/question.html', {'form': form})

def enquete_response_questions(request, enquete_response_id):
    enquete_response = get_object_or_404(EnqueteResponse, id=enquete_response_id)
    enquete = enquete_response.enqueteID
    questions = Question.objects.filter(enqueteID=enquete)
    
    # Vérifier quelles questions ont déjà été répondues
    answered_questions = Question.objects.filter(
        responses__enqueteResponsesID=enquete_response
    ).distinct()
    
    return render(request, 'Responses/questions_list.html', {
        'enquete': enquete,
        'enquete_response': enquete_response,
        'questions': questions,
        'answered_questions': answered_questions
    })
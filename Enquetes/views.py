from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Enquete, EnqueteResponse, Question
from .forms import EnqueteForm, EnqueteResponseForm, QuestionForm

# Liste des enquêtes
@login_required
def enquete_list(request):
    enquetes = Enquete.objects.all()
    return render(request, 'Enquetes/list.html', {'enquetes': enquetes})

# Détails d'une enquête
@login_required
def enquete_detail(request, pk):
    enquete = get_object_or_404(Enquete, id = pk)
    questions = Question.objects.filter(enqueteID=enquete)
    return render(request, 'Enquetes/detail.html', {'enquete': enquete, 'questions': questions})

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
def enquete_update(request, enquete_id):
    enquete = get_object_or_404(Enquete, id=enquete_id)
    if request.method == 'POST':
        form = EnqueteForm(request.POST, instance=enquete)
        if form.is_valid():
            form.save()
            return redirect('enquete_detail', enquete_id=enquete.id)
    else:
        form = EnqueteForm(instance=enquete)
    return render(request, 'Enquetes/forme.html', {'form': form})

# Suppression d'une enquête
@login_required
def enquete_delete(request, enquete_id):
    enquete = get_object_or_404(Enquete, id=enquete_id)
    if request.method == 'POST':
        enquete.delete()
        return redirect('enquete_list')
    return render(request, 'Enquetes/confirm_delete.html', {'enquete': enquete})

# Création d'une réponse à une enquête
def enquete_response_create(request, enquete_id):
    enquete = get_object_or_404(Enquete, id=enquete_id)
    if request.method == 'POST':
        form = EnqueteResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.enqueteID = enquete
            response.save()
            return redirect('enquete_detail', enquete_id=enquete.id)
    else:
        form = EnqueteResponseForm()
    return render(request, 'Enquetes/response_form.html', {'form': form})

# Création d'une question pour une enquête
@login_required
def question_create(request, enquete_id):
    enquete = get_object_or_404(Enquete, id=enquete_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.enqueteID = enquete
            question.save()
            return redirect('enquete_detail', enquete_id=enquete.id)
    else:
        form = QuestionForm()
    return render(request, 'Enquetes/question.html', {'form': form})

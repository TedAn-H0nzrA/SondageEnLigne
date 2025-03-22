from django.shortcuts import render, get_object_or_404, redirect
from .models import Responses, EnqueteResponse, Question, ResponseSelection
from .forms import ResponseForm

def submit_response(request, enquete_response_id, question_id):
    enquete_response = get_object_or_404(EnqueteResponse, id=enquete_response_id)
    question = get_object_or_404(Question, id=question_id)
    
    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.enqueteResponsesID = enquete_response
            response.questionID = question
            response.save()
            return redirect('success_page')  
    else:
        form = ResponseForm()

    return render(request, 'Responses/submit_response.html', {'form': form, 'question': question})

def success_page(request):
    return render(request, 'Responses/success_page.html')
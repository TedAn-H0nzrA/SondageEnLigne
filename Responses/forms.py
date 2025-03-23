from django import forms
from .models import Responses, ResponseSelection

class ResponseForm(forms.ModelForm):
    class Meta:
        model = Responses
        fields = ['responseSelectionID', 'responseComment']
        widgets = {
            'responseComment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ajouter un commentaire (facultatif)'}),
        }
    
    def __init__(self, question, *args, **kwargs):
        super(ResponseForm, self).__init__(*args, **kwargs)
        # Limiter les options de réponse à celles associées à cette question
        self.fields['responseSelectionID'].queryset = ResponseSelection.objects.filter(questionID=question)
        self.fields['responseSelectionID'].label = "Choisissez votre réponse"
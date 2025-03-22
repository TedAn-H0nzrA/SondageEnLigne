from django import forms
from .models import Responses
from Enquetes.models import EnqueteResponse

class ResponseForm(forms.ModelForm):
    class Meta:
        model = Responses
        fields = ['enqueteResponsesID', 'questionID', 'responseSelectionID', 'responseComment']
        widgets = {
            'responseComment': forms.Textarea(attrs = {'rows': 3, 'placeholder' : 'Ajouter un commentaire (facultatif)'}),
        }
from django import forms
from .models import Responses
from Enquetes.models import Question, ResponseSelection, EnqueteResponse

class ResponseForm(forms.ModelForm):
    class Meta:
        model = Responses
        fields = ['responseText', 'responseOptionID']

    def __init__(self, question, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.question = question

        if question.responseType == 'choix_multiple':  # Changed from questionType to responseType
            choices = ResponseSelection.objects.filter(questionID=question)
            self.fields['responseOptionID'] = forms.ModelChoiceField(
                queryset=choices,
                widget=forms.RadioSelect(),
                empty_label=None,
                label="Choisissez votre réponse"
            )
            self.fields.pop('responseText', None)
        else:
            self.fields.pop('responseOptionID', None)
            self.fields['responseText'] = forms.CharField(
                widget=forms.Textarea(attrs={'rows': 4}),
                label="Votre réponse"
            )

class ParticipationForm(forms.ModelForm):
    class Meta:
        model = EnqueteResponse
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Votre adresse email'
            })
        }
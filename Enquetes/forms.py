from django import forms
from .models import Enquete, EnqueteResponse, Question

class EnqueteForm(forms.ModelForm):
    
    class Meta:
        model = Enquete
        fields = ['code', 'name', 'description', 'status', 'endDate']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Code de l\'enquête'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de l\'enquête'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description'}),
            'statut': forms.Select(attrs={'class': 'form-control'}),
            'endDate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class EnqueteResponseForm(forms.ModelForm):
    
    class Meta:
        model = EnqueteResponse
        fields = ['email', 'status']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Votre email'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class QuestionForm(forms.ModelForm):
    
    class Meta:
        model = Question
        fields = ['question', 'description', 'responseType']
        widgets = {
            'question': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Entrez la question'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Détails de la question'}),
            'responseType': forms.Select(attrs={'class': 'form-control'}),
        }
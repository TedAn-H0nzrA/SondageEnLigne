from django.db import models
from Utilisateurs.models import Utilisateurs
from django.utils import timezone
import uuid

# Information à propos de l'enquête, généralement créé par l'utilisateur
class Enquete(models.Model):
    code = models.CharField(max_length = 10)
    name = models.CharField(max_length = 100)
    description = models.CharField(max_length = 255)

    STATUS_CHOICES = [
        ('actif', 'Actif'),
        ('inactif', 'Inactif'),
        ('archive', 'Archivé'),
    ]

    status = models.CharField(max_length = 10,choices = STATUS_CHOICES, default = 'actif')
    startDate = models.DateField(default = timezone.now, editable = False)
    endDate = models.DateField(null = True, blank = True)
    userID = models.ForeignKey(Utilisateurs, on_delete = models.CASCADE)
    token = models.UUIDField(default = uuid.uuid4, editable = False, unique = True)

    def __str__(self):
        return F"({self.name} - ({self.code}))"
    

# Reponse à l'enquête fait par les participants
class EnqueteResponse(models.Model):
    STATUS_CHOICES = [
        ('en_attente', 'En attente'),
        ('complete', 'Completé'),
        ('annule', 'Annuler'),
    ]
    email = models.EmailField(null=True, blank=True)  # Rendre l'email optionnel initialement
    token = models.CharField(max_length=30, unique=True)
    enqueteID = models.ForeignKey(Enquete, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='en_attente')
    responseDatetime = models.DateTimeField(default=timezone.now, editable=False)
    validationDatetime = models.DateTimeField(null=True, blank=True)
    is_email_confirmed = models.BooleanField(default=False)  # Nouveau champ

    def confirm_email(self):
        self.is_email_confirmed = True
        self.save()


    def __str__(self):
        return f"Réponse de {self.email} pour {self.enqueteID.name}"


# Question créée par l'administrateur ou par l'enquêteur
class Question(models.Model):
    TYPE_CHOICES = [
        ('text', 'Texte'),
        ('choix_multiple', 'Choix multiple'),
        ('boolean', 'OUI/NON'),
    ]

    question = models.TextField()
    description = models.TextField()
    enqueteID = models.ForeignKey(Enquete, on_delete = models.CASCADE)
    responseType = models.CharField(max_length = 100, choices = TYPE_CHOICES, default = 'text')

    def __str__(self):
        return f"Question: {self.question[:50]} ..."

# Add this new model for multiple choice options
class ResponseSelection(models.Model):
    questionID = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    option_text = models.CharField(max_length=255)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Option de réponse"
        verbose_name_plural = "Options de réponse"

    def __str__(self):
        return f"{self.option_text} (Question: {self.questionID.question[:30]}...)"
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
    email = models.EmailField(unique = True)
    token = models.CharField(max_length = 30)
    enqueteID = models.ForeignKey(Enquete, on_delete = models.CASCADE)
    status = models.CharField(max_length = 10, choices = STATUS_CHOICES, default = 'en_attente')
    responseDatetime = models.DateTimeField(default = timezone.now, editable = False)
    validationDatetime = models.DateTimeField(null = True, blank = True)

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
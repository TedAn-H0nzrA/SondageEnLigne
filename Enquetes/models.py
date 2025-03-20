from django.db import models
from Utilisateurs.models import Utilisateurs
from django.utils import timezone

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

    statut = models.CharField(max_length = 10,choices = STATUS_CHOICES, default = 'actif')
    startDate = models.DateField(default = timezone.now, editable = False)
    endDate = models.DateField(null = True, blank = True)
    userID = models.ForeignKey(Utilisateurs, on_delete = models.CASCADE)
    token = models.CharField(max_length = 30)

    def __str__(self):
        return self.name
    

# Reponse à l'enquête fait par les participants
class EnqueteResponse(models.Model):
    email = models.EmailField(unique = True)
    token = models.CharField(max_length = 30)
    enqueteID = models.ForeignKey(Enquete, on_delete = models.CASCADE)
    status = models.CharField(max_length = 10)
    responseDatetime = models.DateTimeField(default = timezone.now, editable = False)
    validationDatetime = models.DateTimeField(default = timezone.now, editable = True)


# Question créée par l'administrateur ou par l'enquêteur
class Question(models.Model):
    question = models.TextField()
    description = models.TextField()
    enqueteID = models.ForeignKey(Enquete, on_delete = models.CASCADE)
    responseType = models.CharField(max_length = 100)
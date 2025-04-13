from django.db import models
from django.utils import timezone
from Enquetes.models import Question, ResponseSelection, EnqueteResponse

class Responses(models.Model):
    enqueteResponsesID = models.ForeignKey(EnqueteResponse, on_delete=models.CASCADE)
    questionID = models.ForeignKey(Question, on_delete=models.CASCADE)
    responseText = models.TextField(null=True, blank=True)
    responseOptionID = models.ForeignKey(ResponseSelection, on_delete=models.SET_NULL, null=True, blank=True)
    responseDatetime = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Réponse"
        verbose_name_plural = "Réponses"
        unique_together = ['enqueteResponsesID', 'questionID']

    def __str__(self):
        return f"Réponse de {self.enqueteResponsesID.email} à {self.questionID.question[:30]}..."
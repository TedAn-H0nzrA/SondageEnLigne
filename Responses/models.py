from django.db import models
from Enquetes.models import EnqueteResponse, Question

class ResponseSelection(models.Model):
    response = models.CharField(max_length = 255)
    note = models.IntegerField()
    questionID = models.ForeignKey(Question, on_delete = models.CASCADE)

class Responses(models.Model):
    enqueteResponsesID = models.ForeignKey(EnqueteResponse, on_delete = models.CASCADE)
    questionID = models.ForeignKey(Question, on_delete = models.CASCADE)
    responseSelectionID = models.ForeignKey(ResponseSelection, on_delete = models.CASCADE)
    responseComment = models.TextField(blank = True)

    def __str__(self):
        return f"Response to {self.question}"
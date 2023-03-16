from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Question(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.CharField(max_length=299)
    date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.question
    
class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option = models.CharField(max_length=199)

    def __str__(self):
        return self.option

class Vote(models.Model):
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ['option', 'user']

from django import forms
from .models import *

# Create your forms here.

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question']

class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ['option']

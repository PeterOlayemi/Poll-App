from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView, name='index'),
    path('polls/', QuestionView, name='question'),
    path('poll/answer/<int:pk>/', OptionView, name='option'),
    path('poll/result/<int:pk>/', ResultView, name='result'),
    path('register/', RegisterView, name='register'),
    path('poll/add/', AddPollView, name='add'),
    path('poll/edit/question/<int:pk>/', EditQuestionView, name='editquestion'),
    path('poll/edit/option/<int:pk>/', EditOptionView, name='editoption'),
    path('poll/end/<int:pk>/', EndPollView, name='end'),
    path('poll/option/remove/<int:pk>/', RemoveOptionView, name='remove'),
    path('poll/option/voters/<int:pk>/<int:id>/', ResulterView, name='voter'),
    path('poll/option/add/<int:pk>/', AddOptionView, name='addoption'),
]

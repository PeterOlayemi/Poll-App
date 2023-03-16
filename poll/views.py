from django.shortcuts import render, redirect
from .models import *
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from django.urls import reverse
from django.contrib import messages

# Create your views here.

@login_required
def AddOptionView(request, pk):
    obj = Question.objects.get(id=pk)
    form = OptionForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            data = form.save(commit=False)
            data.question = obj
            data.save()
            messages.success(request, 'Poll edited successfully')
            return redirect(reverse('option', args=[obj.pk]))
    return render(request, 'editquestion.html', {"form":form})

@login_required
def RemoveOptionView(request, pk):
    data = Option.objects.get(id=pk)
    if request.method == 'POST':
        data.delete()
        messages.success(request, 'option deleted')
        return redirect(reverse('option', args=[data.question.pk]))
    return render(request, 'end.html', {'data':data})

@login_required
def EndPollView(request, pk):
    obj = Question.objects.get(id=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'poll ended')
        return redirect('question')
    return render(request, 'end.html', {'obj':obj})

@login_required
def EditOptionView(request, pk):
    obj = Option.objects.get(id=pk)
    form = OptionForm(request.POST or None, instance=obj)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Poll successfully edited')
            return redirect(reverse('option', args=[obj.question.pk]))
    return render(request, 'editquestion.html', {'form':form})

@login_required
def EditQuestionView(request, pk):
    obj = Question.objects.get(id=pk)
    form = QuestionForm(request.POST or None, instance=obj)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Poll successfully edited')
            return redirect(reverse('option', args=[obj.pk]))
    return render(request, 'editquestion.html', {'form':form, 'obj':obj})

@login_required
def AddPollView(request):
    form = QuestionForm(request.POST or None)
    form1 = OptionForm(request.POST or None)
    form2 = OptionForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid() and form1.is_valid() and form2.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            data1 = form1.save(commit=False)
            data1.question = obj
            data1.save()
            data2 = form2.save(commit=False)
            data2.question = obj
            data2.save()
            messages.success(request, 'Poll successfully created')
            return redirect(reverse('option', args=[obj.pk]))
    return render(request, 'add.html', {'form':form, 'form1':form1, 'form2':form2,})

def RegisterView(request):
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful')
            return redirect('login')
    return render(request, 'registration/register.html', {'form':form})

@login_required
def ResulterView(request, pk, id):
    data = Question.objects.get(id=pk)
    obj = Option.objects.filter(question=data).get(id=id)
    cat = Vote.objects.filter(option=obj)
    cat_c = Vote.objects.filter(option=obj).count()
    return render(request, 'resulter.html', {'obj':obj, 'data':data, 'cat':cat, 'cat_c':cat_c})

@login_required
def ResultView(request, pk):
    data = Question.objects.get(id=pk)
    obj = Option.objects.filter(question__id = pk)
    return render(request, 'result.html', {'obj':obj, 'data':data})

def OptionView(request, pk):
    data = Question.objects.get(id=pk)
    obj = Option.objects.filter(question__id = pk)
    vote = Vote.objects.all()
    if request.method == 'POST':
        if request.user.is_authenticated:
            try:
                option = request.POST['option']
                selected = obj.get(id=option)
            except (KeyError, Option.DoesNotExist):
                messages.success(request, 'Invalid Choice')
                return redirect(reverse('option', args=[data.pk]))
            else:
                if vote.filter(option=selected, user=request.user).exists():
                    messages.warning(request, 'vote with this option has been added already')
                    return redirect(reverse('option', args=[data.pk]))
                elif vote.filter(option__question__id = pk, user=request.user).exists():
                    vote.filter(option__question__id = pk, user=request.user).delete()
                    vote.create(option=selected, user=request.user)
                    messages.success(request, 'Vote Changed Successfully')
                    return redirect(reverse('option', args=[data.pk]))
                else:
                    vote.create(option=selected, user=request.user)
                    messages.success(request, 'Vote Added Successfully')
                    return redirect(reverse('option', args=[data.pk]))
        else:
            return redirect(f'/login/?next=/poll/answer/{data.pk}/')
    return render(request, 'option.html', {'obj':obj, 'data':data})

def QuestionView(request):
    obj = Question.objects.all().order_by('-date')
    paginator = Paginator(obj, 5)
    page = request.GET.get('page')
    try:
        obj = paginator.page(page)
    except PageNotAnInteger:
        obj = paginator.page(1)
    except EmptyPage:
        obj = paginator.page(paginator.num_pages)
    return render(request, 'question.html', {'obj':obj})

def HomeView(request):
    return render(request, 'index.html')

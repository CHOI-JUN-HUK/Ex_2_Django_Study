from django.core.checks import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from .models import Answer, Question
from django.utils import timezone
from .forms import QuestionForm, AnswerForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request) :
    page = request.GET.get('page', '1')
    question_list = Question.objects.order_by('-create_date')
    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)
    
    context = {'question_list':page_obj}
    
    return render(request, 'pybo/question_list.html', context)

def detail(request, question_id) :
    question = get_object_or_404(Question, pk=question_id)
    context = {'question':question}

    return render(request, 'pybo/question_detail.html', context)


@login_required(login_url="common:login")
def answer_create(request, question_id) :
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST' :
        form = AnswerForm(request.POST)
        if form.is_valid() :
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.question = question
            answer.author = request.user
            answer.save()
            return redirect('pybo:detail', question_id=question.id)
    else :
        form = AnswerForm()
    context = {'question':question, 'form':form}
    return render(request, 'pybo/question_detail.html', context)


@login_required(login_url="common:login")
def question_create(request) :
    if request.method == 'POST' :
        form = QuestionForm(request.POST)
        if form.is_valid() :
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.author = request.user
            question.save()
            return redirect('pybo:index')
    else:
        form = QuestionForm()
    context = {'form':form}
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url="common:login")
def question_modify(request, question_id) :
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author :
        messages.error(request, '수정 권한이 없습니다.')
        return redirect('pybo:detail', question_id=question.id)
    
    if request.method == 'POST' :
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.modify_date = timezone.now()
            question.save()
            return redirect('pybo:detail', question_id=question.id)
    else :
        form = QuestionForm(instance=question)
    context = {'form':form}
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url="common:login")
def question_delete(request, question_id) :
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    question.delete()
    return redirect('pybo:index')


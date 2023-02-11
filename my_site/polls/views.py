from django.shortcuts import HttpResponse
from django.template import loader
from .models import Question

# Create your views here.

def index(request):
    latest_question_list = reversed(Question.objects.order_by('pub_date')[:5])
    template = loader.get_template('polls/index.html')
    # output = ', '.join([q.question_text for q in latest_question_list])
    context = {
        'latest_question_list': latest_question_list
    }
    return HttpResponse(template.render(context, request))

def detail(request, question_id):
    return HttpResponse(f"You are looking at Question {question_id}")

def results(request, question_id):
    return HttpResponse(f"You are looking at the results of Question {question_id}")

def vote(request, question_id):
    return HttpResponse(f"You are currently voting for Question {question_id}")
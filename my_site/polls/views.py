from django.shortcuts import HttpResponse, render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse
from .models import Question, Choice

# Create your views here.

def index(request):
    latest_question_list = Question.objects.order_by('pub_date')[:5]
    context = {
        'latest_question_list': latest_question_list
    }
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    poll_question = get_object_or_404(Question, id=question_id)
    choices = poll_question.choice_set.all()
    context = {
        'question': poll_question,
        'choices': choices
    }
    return render(request, 'polls/detail.html', context)

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    choices = question.choice_set.all()
    total = sum([choice.votes for choice in choices])
    context = {
        'question': question, 
        'choices': choices,
        'total': total,
        }
    
    return render(request, 'polls/results.html', context)

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': 'You did not select a choice'
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()

        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
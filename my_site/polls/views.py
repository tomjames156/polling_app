from django.shortcuts import render, HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("Hello World, You're at the polls index")

def detail(request, question_id):
    return HttpResponse(f"You are looking at Question {question_id}")

def results(request, question_id):
    return HttpResponse(f"You are looking at the results of Question {question_id}")

def vote(request, question_id):
    return HttpResponse(f"You are currently voting for Question {question_id}")
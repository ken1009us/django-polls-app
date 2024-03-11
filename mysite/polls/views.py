from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello World!")


def detail(request, question_id):
    response = f"You are looking at the question {question_id}."
    return HttpResponse(response)


def results(request, question_id):
    response = f"You are looking at the results of question {question_id}."
    return HttpResponse(response)


def vote(request, question_id):
    return HttpResponse(f"You're voting on question {question_id}.")

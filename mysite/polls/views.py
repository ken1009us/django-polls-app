from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import loader

from .models import Question


def index(request):
    latest_questions_list = Question.objects.order_by("-publish_date")[:5]
    template = loader.get_template("polls/index.html")
    context = {
        "latest_question_list": latest_questions_list,
    }

    return HttpResponse(template.render(context, request))


def detail(request, question_id):
    response = f"You are looking at the question {question_id}."
    return HttpResponse(response)


def results(request, question_id):
    response = f"You are looking at the results of question {question_id}."
    return HttpResponse(response)


def vote(request, question_id):
    return HttpResponse(f"You're voting on question {question_id}.")

"""Defines views for interacting with Ideas"""
from django.http import HttpResponse
from django.shortcuts import render, reverse

from research_assistant.models import Idea

def all_ideas(request):
    ideas = Idea.objects.filter(user=request.user)
    template = "ideas/ideas.html"
    context = {
        "ideas": ideas
    }
    return render(request, template, context)


def single_idea(request):
    return HttpResponse("Single Idea")


def delete_idea(request):
    return HttpResponse("Delete Idea")


def new_idea(request):
    return HttpResponse("New Idea")

"""Defines views for interacting with Ideas"""
from django.http import HttpResponse

from research_assistant.models import Idea

def all_ideas(request):
    return HttpResponse("All Ideas")


def single_idea(request):
    return HttpResponse("Single Idea")


def delete_idea(request):
    return HttpResponse("Delete Idea")


def new_idea(request):
    return HttpResponse("New Idea")

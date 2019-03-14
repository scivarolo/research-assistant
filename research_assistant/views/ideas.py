"""Defines views for interacting with Ideas"""
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, reverse

from research_assistant.forms import IdeaForm
from research_assistant.models import Idea


@login_required
def all_ideas(request):
    ideas = Idea.objects.filter(user=request.user)
    template = "ideas/ideas.html"
    context = {
        "ideas": ideas
    }
    return render(request, template, context)

@login_required
def single_idea(request, idea_id):
    return HttpResponse("Single Idea")

@login_required
def delete_idea(request):
    return HttpResponse("Delete Idea")

@login_required
def new_idea(request):
    """ Handles displaying the new idea form and saving the new idea."""

    if request.method == "POST":
        form_data = request.POST
        title = form_data["title"]
        content = form_data["content"]

        idea = Idea.objects.create(
            title=title,
            content=content,
            user=request.user
        )

        idea.save()

        return HttpResponseRedirect(
            reverse("research_assistant:single_idea", args=(idea.id,))
        )

    template = "ideas/form.html"
    context = {
        "new_idea_form": IdeaForm(),
        "tiny_api_key": settings.TINYMCE_API_KEY,
    }

    return render(request, template, context)

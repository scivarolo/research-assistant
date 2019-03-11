""" Contains all of the views for direct interaction with Tags"""

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse

# from research_assistant.forms import TagForm
from research_assistant.models import Tag


@login_required
def all_tags(request):
    """Load all tags associated with current user."""

    tags = Tag.objects.filter(user=request.user)

    template = "tags/tags.html"
    context = {"tags": tags}

    return render(request, template, context)


@login_required
def single_tag(request):
    pass


@login_required
def new_tag(request):
    pass
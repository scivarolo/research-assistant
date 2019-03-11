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
def single_tag(request, tag_id):
    """ Load the single requested tag, and make sure it is associated with the current user.

        Also handles editing the tag name when the user clicks the edit button next to the name.
    """

    tag = Tag.objects.get(pk=tag_id, user=request.user)
    template = "tags/single.html"
    context = {"tag": tag}

    return render(request, template, context)


@login_required
def new_tag(request):
    pass

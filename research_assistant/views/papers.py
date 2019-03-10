"""
Views for displaying Papers.
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from research_assistant.models import Paper


@login_required
def all_papers(request):
    """Displays a list of all papers."""

    papers = Paper.objects.filter(user=request.user)

    template = "paper/list.html"
    context = {"papers": papers}

    return render(request, template, context)


@login_required
def single_paper(request, paper_id):
    """Displays a single paper."""

    paper = Paper.objects.get(pk=paper_id)
    template = "paper/single.html"
    context = {"paper": paper}

    return render(request, template, context)

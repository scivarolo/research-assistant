"""
Views for displaying Papers.
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Q

from research_assistant.models import Paper
from research_assistant.forms import SearchForm

@login_required
def all_papers(request):
    """Displays a list of all papers."""

    papers = Paper.objects.filter(user=request.user)
    search_form = SearchForm(placeholder="Search by title, tag, or author")
    context = {}

    if request.POST.get("query"):
        query = request.POST["query"]
        if query is not None:
            context["query"] = query
            lookups = Q(title__contains=query) | Q(tags__name__contains=query) | Q(authors__name__contains=query)
            papers = Paper.objects.filter(lookups, user=request.user).distinct()

    template = "paper/list.html"
    context["papers"] = papers
    context["search_form"] = search_form

    return render(request, template, context)


@login_required
def single_paper(request, paper_id):
    """Displays a single paper."""

    paper = Paper.objects.get(pk=paper_id)
    template = "paper/single.html"
    context = {"paper": paper}

    return render(request, template, context)

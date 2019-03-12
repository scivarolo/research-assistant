"""
Views for displaying Papers.
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from research_assistant.models import Paper
from research_assistant.forms import SearchForm, PaperFilterForm

@login_required
def all_papers(request):
    """Displays a list of all papers."""
    print(request)
    papers = Paper.objects.filter(user=request.user)
    search_form = SearchForm(placeholder="Search by title, tag, or author")
    context = {
        "search_form": SearchForm(placeholder="Search by title, tag, or author"),
        "filter_form": PaperFilterForm(user=request.user)
    }

    # The filter form is being cleared
    if request.POST.get("clear"):
        pass

    # Filter the papers
    elif request.method == "POST":
        data = request.POST.copy()
        query = data.get("query")
        tags = data.getlist("tags") if data.getlist("tags") else ""
        lists = data.getlist("lists") if data.getlist("lists") else ""
        authors = data.getlist("authors") if data.getlist("authors") else ""
        is_unread = data.get("is_unread")

        papers = Paper.objects.filter(user=request.user)

        if query != "":
            papers = papers.filter(title__contains=query)

        if tags != "":
            for tag in tags:
                papers = papers.filter(tags__id=tag)

        if lists != "":
            for the_list in lists:
                papers = papers.filter(lists__id=the_list)

        if authors != "":
            for author in authors:
                papers = papers.filter(authors__id=author)

        if is_unread is not None:
            papers = papers.filter(is_read=False)

        context["filter_form"] = PaperFilterForm(data=data, user=request.user)

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

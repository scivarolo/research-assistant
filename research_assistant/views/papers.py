from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.shortcuts import reverse

from research_assistant.models import Paper, Journal, Tag, List, Author

@login_required
def all_papers(request):

    papers = Paper.objects.filter(user=request.user)

    template = "paper/list.html"
    context = {
        "papers": papers
    }

    return render(request, template, context)


@login_required
def single_paper(request, paper_id):

    paper = Paper.objects.get(pk=paper_id)
    template = "paper/single.html"
    context = {
        "paper": paper
    }

    return render(request, template, context)
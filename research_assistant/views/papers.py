from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.shortcuts import reverse
# from django.core.files.storage import FileSystemStorage
# from django.core.exceptions import ValidationError

from research_assistant.models import Paper, Journal, Tag, List, Author
# from research_assistant.forms import AddPaperForm

def all_papers(request):

    papers = Paper.objects.filter(user=request.user)

    template = "paper/list.html"
    context = {
        "papers": papers
    }

    return render(request, template, context)


def single_paper(request, paper_id):

    paper = Paper.objects.get(pk=paper_id)
    template = "paper/single.html"
    context = {
        "paper": paper
    }

    return render(request, template, context)
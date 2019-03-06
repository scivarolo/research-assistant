from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import reverse
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ValidationError

from research_assistant.models import Paper, Journal, Tag, List, Author
from research_assistant.forms import AddPaperForm

@login_required
def add_paper(request):
    """ Handles displaying the Add Paper form and saving a paper to the database. """

    if request.method == "GET":
        paper_form = AddPaperForm(request.user)
        template_name = "paper/add.html"
        context = {
            "paper_form": paper_form,
            "file_error": False
        }
        return render(request, template_name, context)

    elif request.method == "POST":
        form_data = request.POST
        paper_form = AddPaperForm(request.user, form_data)

        title = form_data["title"]
        source_url = form_data["source_url"]
        file_url = form_data["file_url"]
        date_published = form_data["date_published"]
        journal = Journal.objects.get(pk=form_data["journal"])
        paper = Paper.objects.create(
            user=request.user,
            title=title,
            source_url=source_url,
            file_url=file_url,
            date_published=date_published,
            journal=journal,
        )

        # Loop through submitted tags and add existing, or create a new one
        tags = form_data.getlist("tags")
        for tag in tags:
            try:
                paper.tags.add(Tag.objects.get(pk=tag))
            except:
                paper.tags.add(Tag.objects.create(name=tag, user=request.user))

        # Loop through submitted lists and add existing, or create a new one
        lists = form_data.getlist("lists")
        for list in lists:
            try:
                paper.lists.add(List.objects.get(pk=list))
            except:
                paper.lists.add(List.objects.create(name=list, user=request.user))

        # Loop through submitted authors and add existing, or create a new one
        authors = form_data.getlist("authors")
        for author in authors:
            try:
                paper.authors.add(Author.objects.get(pk=author))
            except:
                paper.authors.add(Author.objects.create(name=author, user=request.user))

        paper.save()

        return HttpResponseRedirect(reverse("research_assistant:single_paper", args=(paper.id,)))

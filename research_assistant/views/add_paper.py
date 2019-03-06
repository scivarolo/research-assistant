import os

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import reverse
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ValidationError
from django.conf import settings

from research_assistant.models import Paper, Journal, Tag, List, Author
from research_assistant.forms import AddPaperForm

@login_required
def add_paper(request):
    """ Handles displaying the Add Paper form and saving a paper to the database. """

    # Load the form
    if request.method == "GET":
        paper_form = AddPaperForm(request.user)
        template_name = "paper/add.html"
        context = {
            "paper_form": paper_form,
            "file_error": False
        }
        return render(request, template_name, context)

    # Save the form data
    elif request.method == "POST":
        form_data = request.POST
        paper_form = AddPaperForm(request.user, form_data)

        # save the uploaded PDF to the user's media directory
        uploaded_file_url = ""
        if "file_url" in request.FILES:
            directory = os.path.join(settings.MEDIA_ROOT, str(request.user.id))
            url = settings.MEDIA_URL + str(request.user.id)
            file = request.FILES["file_url"]
            fs = FileSystemStorage(directory, base_url=url)
            uploaded_file = fs.save(file.name, file)
            uploaded_file_url = fs.url(uploaded_file)

        title = form_data["title"]
        source_url = form_data["source_url"]
        file_url = uploaded_file_url
        date_published = form_data["date_published"]
        is_read = True if form_data["is_read"] == "on" else False

        # See if journal exists in db or is new.
        try:
            journal = Journal.objects.get(pk=form_data["journal"])
        except:
            journal = Journal.objects.create(name=form_data["journal"], user=request.user)

        # Create Paper Object
        paper = Paper.objects.create(
            user=request.user,
            title=title,
            source_url=source_url,
            file_url=file_url,
            date_published=date_published,
            journal=journal,
            is_read=is_read
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

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
        file = None
        if "file_url" in request.FILES:
            file = request.FILES["file_url"]

        title = form_data["title"]
        source_url = form_data["source_url"]
        file_url = file
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


@login_required
def edit_paper(request, paper_id):

    # Load the form
    if request.method == "GET":
        paper = Paper.objects.get(pk=paper_id)
        paper_form = AddPaperForm(request.user, instance=paper)
        template_name = "paper/edit.html"
        context = {
            "paper_form": paper_form,
            "paper_id": paper_id,
            "file_error": False
        }
        return render(request, template_name, context)

    elif request.method == "POST":
        form_data = request.POST
        paper = Paper.objects.get(pk=paper_id)

        # if clear is checked, delete the existing file
        if "file_url-clear" in form_data:
            paper.file_url.delete()
            paper.file_url = None

        # if new file is uploaded, delete the possible existing file first
        if "file_url" in request.FILES:
            paper.file_url.delete()
            file = request.FILES["file_url"]
            paper.file_url = file

        paper.title = form_data["title"]
        paper.source_url = form_data["source_url"]
        paper.date_published = form_data["date_published"]
        # paper.file_url = file
        try:
            paper.journal = Journal.objects.get(pk=form_data["journal"])
        except:
            paper.journal = Journal.objects.create(name=form_data["journal"], user=request.user)

        # Save changes to paper
        paper.save()

        # check if tags were changed. remove or add as needed
        new_tags = form_data.getlist("tags")
        old_tags = paper.tags.all()

        # compare new list with old list
        # if old tag is not in new list, remove the relation
        # if old tag is in new list, remove it from the list, to be left with only new tags to add
        for old_tag in old_tags:
            if str(old_tag.id) not in new_tags:
                instance = Tag.objects.get(pk=old_tag.id)
                paper.tags.remove(instance)

            elif str(old_tag.id) in new_tags:
                new_tags.remove(str(old_tag.id))

        # Add the remaining tags
        for tag in new_tags:
            try:
                paper.tags.add(Tag.objects.get(pk=tag))
            except:
                paper.tags.add(Tag.objects.create(name=tag, user=request.user))

        # Repeat process for authors
        new_authors = form_data.getlist("authors")
        old_authors = paper.authors.all()

        for old_author in old_authors:
            if str(old_author.id) not in new_authors:
                instance = Author.objects.get(pk=old_author.id)
                paper.authors.remove(instance)

            elif str(old_author.id) in new_authors:
                new_authors.remove(str(old_author.id))

        # Add the remaining authors
        for author in new_authors:
            try:
                paper.authors.add(Author.objects.get(pk=author))
            except:
                paper.authors.add(Author.objects.create(name=author, user=request.user))

        # Repeat process for lists
        new_lists = form_data.getlist("lists")
        old_lists = paper.lists.all()

        for old_list in old_lists:
            if str(old_list.id) not in new_lists:
                instance = List.objects.get(pk=old_list.id)
                paper.lists.remove(instance)

            elif str(old_list.id) in new_lists:
                new_lists.remove(str(old_list.id))

        # Add the remaining lists
        for list in new_lists:
            try:
                paper.lists.add(List.objects.get(pk=list))
            except:
                paper.lists.add(List.objects.create(name=list, user=request.user))

        return HttpResponseRedirect(reverse("research_assistant:single_paper", args=(paper.id,)))

""" Contains all of the views for direct interaction with Authors """

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse

from research_assistant.forms import AuthorForm
from research_assistant.models import Author


@login_required
def all_authors(request):
    """Load all authors associated with current user."""

    authors = Author.objects.filter(user=request.user)

    template = "authors/authors.html"
    context = {"authors": authors}

    return render(request, template, context)


@login_required
def single_author(request, author_id):
    """ Load the single requested author, if associated with current user.

    Also handles editing the author name when edit button is clicked.
    """
    author = Author.objects.get(pk=author_id, user=request.user)
    template = "authors/single.html"
    context = {"author": author}

    if request.method == "GET" and request.GET.get("edit"):
        edit_author_form = AuthorForm(instance=author)
        context = {
            "author": author,
            "edit_author_form": edit_author_form
        }

    elif request.method == "POST":
        author.name = request.POST["name"]
        author.save()

    return render(request, template, context)


@login_required
def new_author(request):
    """ Creates a new author."""

    if request.method == "POST":
        name = request.POST["name"]
        author = Author.objects.create(name=name, user=request.user)
        author.save()
        return HttpResponseRedirect(
            reverse("research_assistant:single_author", args=(author.id,))
        )

    template = "authors/new.html"
    context = {"new_author_form": AuthorForm()}

    return render(request, template, context)


@login_required
def delete_author(request, author_id):
    """ Displays a confirmation page that only lets the user delete an Author if no Paper's are related to them."""

    pass
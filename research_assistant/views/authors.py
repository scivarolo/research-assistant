""" Contains all of the views for direct interaction with Authors """

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.db.models import Prefetch

from research_assistant.forms import AuthorForm, SearchForm
from research_assistant.models import Author, Paper


@login_required
def all_authors(request):
    """Load all authors associated with current user."""

    authors = Author.objects.filter(user=request.user)
    context = {"search_form": SearchForm(placeholder="Search authors")}

    # Update query if a search is submitted
    if request.POST.get("query"):
        query = request.POST["query"]
        if query is not None:
            context["query"] = query
            authors = Author.objects.filter(name__contains=query, user=request.user)

    template = "authors/authors.html"
    context["authors"] = authors

    return render(request, template, context)


@login_required
def single_author(request, author_id):
    """ Load the single requested author, if associated with current user.

    Also handles editing the author name when edit button is clicked.
    """
    author = Author.objects.get(pk=author_id, user=request.user)
    template = "authors/single.html"
    context = {"search_form": SearchForm(placeholder="Search papers by this author")}

    # if searching
    if request.POST.get("query"):
        query = request.POST["query"]
        if query is not None:
            context["query"] = query
            # Prefetch the papers in the query
            papers = Paper.objects.filter(title__contains=query, user=request.user)
            author = (
                Author.objects.filter(pk=author_id, user=request.user)
                .prefetch_related(Prefetch("paper_set", queryset=papers))
                .get()
            )

    # if requestiong edit
    if request.method == "GET" and request.GET.get("edit"):
        context["edit_author_form"] = AuthorForm(instance=author)

    # if saving edit
    elif request.POST.get("name"):
        author.name = request.POST["name"]
        author.save()

    context["author"] = author

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

    author = Author.objects.get(pk=author_id, user=request.user)

    if request.method == "POST":
        author.delete()
        return HttpResponseRedirect(reverse("research_assistant:all_authors"))

    template = "authors/delete.html"
    context = {"author": author}
    return render(request, template, context)

""" Contains all of the views pertaining to Lists """

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse

from research_assistant.forms import ListForm, SearchForm
from research_assistant.models import List


@login_required
def all_lists(request):
    """ Load all lists associated with user. """

    lists = List.objects.filter(user=request.user)
    search_form = SearchForm(placeholder="Search lists")
    context = {}

    # Update query if a search is submitted
    if request.POST.get("query"):
        query = request.POST["query"]
        if query is not None:
            context["query"] = query
            lists = List.objects.filter(name__contains=query, user=request.user)

    template = "lists/lists.html"
    context["lists"] = lists
    context["search_form"] = search_form

    return render(request, template, context)


@login_required
def single_list(request, list_id):
    """ Load the single request list, and make sure it is associated with the current user.

        Also handles editing the list's name when the user clicks the edit button next to the name.
    """

    the_list = List.objects.get(pk=list_id, user=request.user)
    template = "lists/single.html"
    context = {"list": the_list}

    if request.method == "GET" and request.GET.get("edit"):
        edit_list_form = ListForm(instance=the_list)
        context = {"list": the_list, "edit_list_form": edit_list_form}

    elif request.method == "POST":
        the_list.name = request.POST["name"]
        the_list.save()

    return render(request, template, context)


@login_required
def delete_list(request, list_id):
    """ Delete a list and remove the relationships to papers."""

    the_list = List.objects.get(pk=list_id, user=request.user)

    if request.method == "GET":
        template = "lists/delete.html"
        context = {"list": the_list}
        return render(request, template, context)

    elif request.method == "POST":
        the_list.delete()
        return HttpResponseRedirect(reverse("research_assistant:all_lists"))


@login_required
def new_list(request):
    """ Create a new list. """

    if request.method == "POST":
        name = request.POST["name"]
        the_list = List.objects.create(name=name, user=request.user)
        the_list.save()
        return HttpResponseRedirect(
            reverse("research_assistant:single_list", args=(the_list.id,))
        )

    template = "lists/new.html"
    context = {"new_list_form": ListForm()}

    return render(request, template, context)

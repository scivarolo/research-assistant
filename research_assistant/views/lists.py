""" Contains all of the views pertaining to Lists """

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.db.models import Prefetch

from research_assistant.forms import ListForm, SearchForm, PaperFilterForm
from research_assistant.models import List, Paper
from research_assistant.utils import __filter_papers_query

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
    papers = Paper.objects.filter(user=request.user, lists__id=list_id)
    template = "lists/single.html"
    context = {
        "filter_form": PaperFilterForm(user=request.user, current_list=list_id),
        "papers": papers
    }

    # The filter form is being cleared
    if request.POST.get("clear"):
        pass

    # if saving edit
    elif request.POST.get("name"):
        the_list.name = request.POST["name"]
        the_list.save()

    # Filter the papers within the list
    elif request.method == "POST":
        data = request.POST.copy()

        # Build the Paper query with the filters applied
        filtered_papers = __filter_papers_query(data, request.user)
        filtered_papers = filtered_papers.filter(lists__id=list_id)

        # the_list = (
        #     List.objects.filter(pk=list_id, user=request.user)
        #     .prefetch_related(Prefetch("paper_set", queryset=papers))
        #     .get()
        # )
        context["papers"] = filtered_papers
        context["filter_form"] = PaperFilterForm(data=data, user=request.user, current_list=list_id)

    # if requesting edit
    elif request.method == "GET" and request.GET.get("edit"):
        context["edit_list_form"] = ListForm(instance=the_list)


    context["list"] = the_list

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

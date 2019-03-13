""" Contains all of the views for direct interaction with Tags"""

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.db.models import Prefetch

from research_assistant.forms import SearchForm, TagForm, PaperFilterForm
from research_assistant.models import Tag, Paper
from research_assistant.utils import __filter_papers_query


@login_required
def all_tags(request):
    """Load all tags associated with current user."""

    tags = Tag.objects.filter(user=request.user)
    context = {"search_form": SearchForm(placeholder="Search tags")}

    # Update query if a search is submitted
    if request.POST.get("query"):
        query = request.POST["query"]
        if query is not None:
            context["query"] = query
            tags = Tag.objects.filter(name__contains=query, user=request.user)

    template = "tags/tags.html"
    context["tags"] = tags

    return render(request, template, context)


@login_required
def single_tag(request, tag_id):
    """ Load the single requested tag, and make sure it is associated with the current user.

        Also handles editing the tag name when the user clicks the edit button next to the name.
    """
    tag = Tag.objects.get(pk=tag_id, user=request.user)
    papers = Paper.objects.filter(user=request.user, tags__id=tag_id)

    template = "tags/single.html"
    context = {
        "filter_form": PaperFilterForm(user=request.user, current_tag=tag_id),
        "papers": papers}

    # The filter form is being cleared
    if request.POST.get("clear"):
        pass

    # if saving edit
    elif request.POST.get("name"):
        tag.name = request.POST["name"]
        tag.save()

    elif request.method == "POST":
        data = request.POST.copy()
        filtered_papers = __filter_papers_query(data, request.user)
        filtered_papers = filtered_papers.filter(tags__id=tag_id)
        # tag = (
        #     Tag.objects.filter(pk=tag_id, user=request.user)
        #     .prefetch_related(Prefetch("paper_set", queryset=papers))
        #     .get()
        # )
        context["papers"] = filtered_papers
        context["filter_form"] = PaperFilterForm(data=data, user=request.user, current_tag=tag_id)


    # if requesting edit
    elif request.method == "GET" and request.GET.get("edit"):
        context["edit_tag_form"] = TagForm(instance=tag)

    context["tag"] = tag

    return render(request, template, context)


@login_required
def new_tag(request):
    """ Creates a new tag. """

    if request.method == "POST":
        name = request.POST["name"]
        tag = Tag.objects.create(name=name, user=request.user)
        tag.save()
        return HttpResponseRedirect(
            reverse("research_assistant:single_tag", args=(tag.id,))
        )

    template = "tags/new.html"
    context = {"new_tag_form": TagForm()}

    return render(request, template, context)


@login_required
def delete_tag(request, tag_id):
    """ Delete a tag and remove the relationships to papers."""

    tag = Tag.objects.get(pk=tag_id, user=request.user)

    if request.method == "POST":
        tag.delete()
        return HttpResponseRedirect(reverse("research_assistant:all_tags"))

    template = "tags/delete.html"
    context = {"tag": tag}
    return render(request, template, context)

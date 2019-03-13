"""Contains utility functions for research_assistant"""
from .models import Paper

def __filter_papers_query(data, user):
    """ Constructs the Paper filter query with the options selected from a PaperFilterForm

        Params:
            data -- form data from request.POST
            user -- the user that made the request

        Returns:
            papers -- Paper query with filters applied
    """
    query = data.get("query")
    tags = data.getlist("tags") if data.getlist("tags") else ""
    lists = data.getlist("lists") if data.getlist("lists") else ""
    authors = data.getlist("authors") if data.getlist("authors") else ""
    is_unread = data.get("is_unread")

    papers = Paper.objects.filter(user=user)

    if query != "":
        papers = papers.filter(title__contains=query)

    if tags != "":
        for tag in tags:
            papers = papers.filter(tags__id=tag)

    if lists != "":
        for the_list in lists:
            papers = papers.filter(lists__id=the_list)

    if authors != "":
        for author in authors:
            papers = papers.filter(authors__id=author)

    if is_unread is not None:
        papers = papers.filter(is_read=False)

    return papers
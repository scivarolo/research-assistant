"""Displays the home page."""

from django.shortcuts import render


def index(request):
    """Displays the main index."""
    template_name = "index.html"
    return render(request, template_name)

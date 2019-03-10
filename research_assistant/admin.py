"""Adds the app's models to the admin view."""

from django.contrib import admin
from .models import Paper, Tag, List, Author, Journal, Note

# Register your models here.
admin.site.register(Paper)
admin.site.register(Tag)
admin.site.register(List)
admin.site.register(Author)
admin.site.register(Journal)
admin.site.register(Note)

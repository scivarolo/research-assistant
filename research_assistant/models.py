"""
Defines all models for research_assistant
"""

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from tinymce.models import HTMLField


def upload_to(instance, filename):
    """Include user id as subfolder for media upload"""
    return str(instance.user.id) + "/" + filename


class Paper(models.Model):
    """Defines a model for a research Paper."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    source_url = models.URLField()
    file_url = models.FileField(upload_to=upload_to, null=True, blank=True)
    date_added = models.DateTimeField(default=timezone.now)
    date_published = models.DateField()
    journal = models.ForeignKey("Journal", on_delete=models.PROTECT)
    tags = models.ManyToManyField("Tag", blank=True)
    lists = models.ManyToManyField("List", blank=True)
    authors = models.ManyToManyField("Author", blank=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title}"


class Tag(models.Model):
    """Defines the Tag model. Used to organize Papers and Ideas."""

    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"


class List(models.Model):
    """Defines the List model. Used to group Papers together."""

    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def unread_count(self):
        """Returns the number of unread papers in a list."""
        return Paper.objects.filter(lists=self, is_read=False).count()

    def __str__(self):
        return f"{self.name}"


class Author(models.Model):
    """Defines the Author model. Used for Authors of Papers."""

    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"


class Journal(models.Model):
    """Defines the Journal model. Contains the source Journal information for Papers."""

    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"


class Note(models.Model):
    """Note is always linked to a Paper"""

    paper = models.ForeignKey("Paper", on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=True, null=True)
    content = HTMLField()
    date_created = models.DateTimeField(default=timezone.now)
    date_modified = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ("-date_modified",)

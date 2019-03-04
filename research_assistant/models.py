import datetime
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

# Create your models here.

class Paper(models.Model):
    """Defines a model for a research Paper."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    source_url = models.URLField()
    file_url = models.FileField(null=True, blank=True)
    date_added = models.DateTimeField(default=timezone.now)
    date_published = models.DateField()
    journal = models.ForeignKey("Journal", on_delete=models.PROTECT)
    tags = models.ManyToManyField("Tag")
    lists = models.ManyToManyField("List")
    authors = models.ManyToManyField("Author")


class Tag(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class List(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Author(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Journal(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
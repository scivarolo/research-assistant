"""
Contains all of the forms used in research_assistant.
"""

from crispy_forms.bootstrap import FieldWithButtons
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms
from django.contrib.auth.models import User
from django_select2.forms import Select2MultipleWidget, Select2Widget

from .models import Author, Journal, List, Note, Paper, Tag


class UserForm(forms.ModelForm):
    """ Form for registering new users. """

    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ("username", "email", "password", "first_name", "last_name")


class AddPaperForm(forms.ModelForm):
    """Form for adding a new paper at papers/add/ """

    is_read = forms.BooleanField(initial=False, required=False, label="Mark as read")

    class Meta:
        model = Paper
        fields = (
            "title",
            "source_url",
            "file_url",
            "date_published",
            "journal",
            "tags",
            "lists",
            "authors",
            "is_read",
        )
        widgets = {
            "journal": Select2Widget(attrs={"data-tags": "true"}),
            "tags": Select2MultipleWidget(
                attrs={"data-tags": "true", "data-token-separators": "[',']"}
            ),
            "lists": Select2MultipleWidget(
                attrs={"data-tags": "true", "data-token-separators": "[',']"}
            ),
            "authors": Select2MultipleWidget(
                attrs={"data-tags": "true", "data-token-separators": '[","]'}
            ),
            "date_published": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, user, *args, **kwargs):
        super(AddPaperForm, self).__init__(*args, **kwargs)
        self.fields["tags"].queryset = Tag.objects.filter(user=user)
        self.fields["lists"].queryset = List.objects.filter(user=user)
        self.fields["authors"].queryset = Author.objects.filter(user=user)
        self.fields["journal"].queryset = Journal.objects.filter(user=user)
        self.helper = FormHelper()
        self.helper.add_input(Submit("submit", "Save Paper"))


class PaperNoteForm(forms.ModelForm):
    """Form for creating new notes and editing existing notes"""

    class Meta:
        model = Note
        fields = ("title", "content")


class ListForm(forms.ModelForm):
    """Form for creating a new list or editing a list's name"""

    class Meta:
        model = List
        fields = ("name",)


class TagForm(forms.ModelForm):
    """Form for creating a new tag or editing a tag's name"""

    class Meta:
        model = Tag
        fields = ("name",)


class AuthorForm(forms.ModelForm):
    """Form for creating a new author or editing an existing Author's name"""

    class Meta:
        model = Author
        fields = ("name",)


class SearchForm(forms.Form):
    """ Generates a generic search form. """

    query = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Search"}
        ),
        label="",
    )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            FieldWithButtons("query", Submit("submit", "Search"))
        )
        super(SearchForm, self).__init__(*args, **kwargs)
        placeholder = kwargs.pop("placeholder", None)
        if placeholder:
            self.fields["query"].widget.attrs.update({"placeholder": placeholder})

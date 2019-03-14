"""
Contains all of the forms used in research_assistant.
"""

from crispy_forms.bootstrap import FieldWithButtons
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div
from django import forms
from django.contrib.auth.models import User
from django_select2.forms import Select2MultipleWidget, Select2Widget

from .models import Author, Journal, List, Note, Paper, Tag, Idea


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


class IdeaForm(forms.ModelForm):
    """Form for creating new ideas and editing existing ideas"""

    class Meta:
        model = Idea
        fields = ("title", "content")


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
        placeholder = kwargs.pop("placeholder", None)
        super(SearchForm, self).__init__(*args, **kwargs)
        if placeholder:
            self.fields["query"].widget.attrs.update({"placeholder": placeholder})


class PaperFilterForm(forms.ModelForm):
    """ Form for filtering papers by query, tag, list, author, unread

        kwargs --
            current_list [int] -- exclude the provided id from the dropdown
            current_author [int] -- exclude the provided id from the dropdown
            current_tag [int] -- exclude the provided id from the dropdown
    """
    is_unread = forms.BooleanField(initial=False, required=False, label="Show unread papers only")
    query = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Search by title"}
        ), required=False
    )
    class Meta:
        model = Paper
        fields = (
            "query",
            "tags",
            "lists",
            "authors",
            "is_unread",
        )
        widgets = {
            "tags": Select2MultipleWidget(
                attrs={"data-token-separators": "[',']"}
            ),
            "lists": Select2MultipleWidget(
                attrs={"data-token-separators": "[',']"}
            ),
            "authors": Select2MultipleWidget(
                attrs={"data-token-separators": '[","]'}
            )
        }

    def __init__(self, user, *args, **kwargs):
        current_list = kwargs.pop("current_list", None)
        current_tag = kwargs.pop("current_tag", None)
        current_author = kwargs.pop("current_author", None)

        super(PaperFilterForm, self).__init__(*args, **kwargs)

        # Set up tag query, check if current_tag kwarg supplied
        tag_query = Tag.objects.filter(user=user)
        if current_tag is not None:
            tag_query = tag_query.exclude(pk=current_tag)
        self.fields["tags"].queryset = tag_query

        # Set up list query, check if current_list kwarg supplied
        list_query = List.objects.filter(user=user)
        if current_list is not None:
            list_query = list_query.exclude(pk=current_list)
        self.fields["lists"].queryset = list_query

        # Set up author query, check if current_author kwarg supplied
        author_query = Author.objects.filter(user=user)
        if current_author is not None:
            author_query = author_query.exclude(pk=current_author)
        self.fields["authors"].queryset = author_query

        self.helper = FormHelper()
        self.helper.add_input(Submit("submit", "Filter"))
        self.helper.add_input(Submit("clear", "Clear"))
        self.helper.layout = Layout(
            Div(
                Div(
                    "query",
                    css_class="col"
                ),
                Div(
                    "tags",
                    css_class="col"
                ),
                Div(
                    "lists",
                    css_class="col"
                ),
                Div(
                    "authors",
                    "is_unread",
                    css_class="col"
                ),
                css_class="row",
            )
        )

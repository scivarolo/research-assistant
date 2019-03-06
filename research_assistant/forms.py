from django import forms
from django.contrib.auth.models import User

from django_select2.forms import Select2TagWidget, Select2Widget, Select2MultipleWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Paper, Tag, List, Author

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ("username", "email", "password", "first_name", "last_name")


class AddPaperForm(forms.ModelForm):
    """ Form for adding a new paper at papers/add/ """

    class Meta:
        model = Paper
        fields = ("title", "source_url", "file_url", "date_published", "journal", "tags", "lists", "authors")
        widgets = {
            "journal": Select2Widget(attrs={"data-tags": "true"}),
            "tags": Select2MultipleWidget(attrs={
                "data-tags": "true",
                "data-token-separators": "[',']",
            }),
            "lists": Select2MultipleWidget(attrs = {
                "data-tags": "true",
                "data-token-separators": "[',']",
            }),
            "authors": Select2MultipleWidget(attrs={
                "data-tags": "true",
                "data-token-separators": '[","]',
            }),
            "date_published": forms.DateInput(attrs={"type": "date"})
        }

    def __init__(self, user, *args, **kwargs):
        super(AddPaperForm, self).__init__(*args, **kwargs)
        self.fields['tags'].queryset = Tag.objects.filter(user=user)
        self.fields['lists'].queryset = List.objects.filter(user=user)
        self.fields['authors'].queryset = Author.objects.filter(user=user)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Save Paper'))
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.conf import settings
from django.utils import timezone

from research_assistant.models import Note, Paper
from research_assistant.forms import PaperNoteForm

@login_required
def add_note(request, paper_id):

    if request.method == "GET":

        paper = Paper.objects.get(pk=paper_id)
        note_form = PaperNoteForm()
        template = "paper/note.html"
        context = {
            "paper": paper,
            "note_form": note_form,
            "tiny_api_key": settings.TINYMCE_API_KEY
        }

        return render(request, template, context)

    elif request.method == "POST":

        form_data = request.POST
        title = form_data["title"]
        content = form_data["content"]

        note = Note.objects.create(
            title=title,
            content=content,
            paper=Paper.objects.get(pk=paper_id),
            user=request.user
        )

        note.save()

        return HttpResponseRedirect(reverse("research_assistant:single_paper", args=(paper_id,)))


@login_required
def edit_note(request, paper_id, note_id):

    if request.method == "GET":

        paper = Paper.objects.get(pk=paper_id)
        note = Note.objects.get(pk=note_id)
        note_form = PaperNoteForm(instance=note)
        template = "paper/note.html"
        context = {
            "paper": paper,
            "note": note,
            "note_form": note_form,
            "tiny_api_key": settings.TINYMCE_API_KEY
        }

        return render(request, template, context)

    elif request.method == "POST":

        form_data = request.POST
        title = form_data["title"]
        content = form_data["content"]

        note = Note.objects.get(pk=note_id)
        print(note_id)
        note.title = title
        note.content = content
        note.date_modified = timezone.now()
        note.save()

        return HttpResponseRedirect(reverse("research_assistant:single_paper", args=(paper_id,)))


def delete_note(request, paper_id, note_id):

    if request.method == "GET":
        note = Note.objects.get(pk=note_id)
        template = "paper/delete_note.html"
        context = {
            "note": note
        }
        return render(request, template, context)

    elif request.method == "POST":
        note = Note.objects.get(pk=note_id)
        note.delete()

        return HttpResponseRedirect(reverse("research_assistant:single_paper", args=(paper_id,)))

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import reverse
from django.conf import settings

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
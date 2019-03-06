from django.urls import path
from . import views

app_name = "research_assistant"

urlpatterns = [
    path("", views.index, name="index"),
    path("papers/add/", views.add_paper, name="add_paper")
]
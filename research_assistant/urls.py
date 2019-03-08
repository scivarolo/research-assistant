from django.urls import path
from . import views

app_name = "research_assistant"

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("register/", views.register_user,  name="register"),
    path("papers/", views.all_papers, name="all_papers"),
    path("papers/<int:paper_id>", views.single_paper, name="single_paper"),
    path("papers/<int:paper_id>/edit/", views.edit_paper, name="edit_paper"),
    path("papers/<int:paper_id>/delete/", views.delete_paper, name="delete_paper"),
    path("papers/<int:paper_id>/notes/add/", views.add_note, name="add_note"),
    path("papers/<int:paper_id>/notes/<int:note_id>/edit/", views.edit_note, name="edit_note"),
    path("papers/<int:paper_id>/notes/<int:note_id>/delete/", views.delete_note, name="delete_note"),
    path("papers/add/", views.add_paper, name="add_paper"),
]
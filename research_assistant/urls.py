"""
All url patterns for research_assistant.
"""

from django.urls import path

from . import views

app_name = "research_assistant"

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("register/", views.register_user, name="register"),
    # Paper Views
    path("papers/", views.all_papers, name="all_papers"),
    path("papers/<int:paper_id>/", views.single_paper, name="single_paper"),
    path("papers/<int:paper_id>/edit/", views.edit_paper, name="edit_paper"),
    path("papers/<int:paper_id>/delete/", views.delete_paper, name="delete_paper"),
    path("papers/<int:paper_id>/notes/add/", views.add_note, name="add_note"),
    path(
        "papers/<int:paper_id>/notes/<int:note_id>/edit/",
        views.edit_note,
        name="edit_note",
    ),
    path(
        "papers/<int:paper_id>/notes/<int:note_id>/delete/",
        views.delete_note,
        name="delete_note",
    ),
    path("papers/add/", views.add_paper, name="add_paper"),
    # List Views
    path("lists/", views.all_lists, name="all_lists"),
    path("lists/<int:list_id>/", views.single_list, name="single_list"),
    path("lists/<int:list_id>/delete/", views.delete_list, name="delete_list"),
    path("lists/new/", views.new_list, name="new_list"),
    # Tag Views
    path("tags/", views.all_tags, name="all_tags"),
    path("tags/<int:tag_id>/", views.single_tag, name="single_tag"),
    path("tags/<int:tag_id>/delete/", views.delete_tag, name="delete_tag"),
    path("tags/new/", views.new_tag, name="new_tag"),
    path("authors/", views.all_authors, name="all_authors"),
    path("authors/<int:author_id>/", views.single_author, name="single_author"),
    path("authors/<int:author_id>/delete", views.delete_author, name="delete_author"),
    path("authors/new/", views.new_author, name="new_author"),
]

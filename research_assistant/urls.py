from django.urls import path
from . import views

app_name = "research_assistant"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_user, name="login"),
    path("logout", views.logout_user, name="logout"),
    path("register", views.register_user,  name="register")
]
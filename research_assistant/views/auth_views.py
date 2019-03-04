from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.template import RequestContext
from django.urls import reverse
from django.contrib import messages

from research_assistant.forms import UserForm

def register_user(request):
    """Handles the creation of a new user

    Method arguments:
        request -- The full HTTP request object
    """

    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            registered = True

        print("Successfully registered")
        return login_user(request)

    elif request.method == "GET":
        user_form = UserForm()
        template_name = "register.html"
        context = {"user_form": user_form}
        return render(request, template_name, context)


def login_user(request):
    """Handles authenticating a user

    Method arguments:
        request -- The full HTTP request object
    """
    print("we loggin in")
    context = {"next": request.GET.get("next", "/")}

    if request.method == "POST":
        print(request.POST)
        username = request.POST["username"]
        password = request.POST["password"]
        authenticated_user = authenticate(username=username, password=password)

        if authenticated_user is not None:
            login(request=request, user=authenticated_user)
            if request.POST.get("next") == "/":
                return HttpResponseRedirect("/")
            else:
                print("We in this")
                return HttpResponseRedirect(request.POST.get("next", "/"))

        else:
            messages.error(request, "Login Failed. Your username or password is incorrect.")

    return render(request, "login.html", context)


@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")
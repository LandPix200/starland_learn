from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpRequest
from .models import User
from django.db import IntegrityError
from django.contrib.auth import (
    authenticate,
    login as django_login,
    logout as django_logout,
)


def login(request: HttpRequest):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        user = authenticate(request, username=email, password=password)

        if user is not None:
            django_login(request, user)
            return redirect("home")
        else:
            return render(
                request,
                "users/login.html",
                context={"error": "Email ou mot de passe incorrect"},
            )

    return render(request, "users/login.html")


def register(request):
    if request.method == "POST":
        try:
            user = User.objects.create_user(
                email=request.POST["email"],
                last_name=request.POST["name"],
                password=request.POST["password"],
                phone_number=request.POST["phone"],
                country=request.POST["country"],
                city=request.POST["city"],
            )

            django_login(request, user)
            return redirect("index")
        except IntegrityError:
            return render(
                request,
                "users/signup.html",
                context={"email_unique_error": "Email déjà utilisé"},
            )

        except Exception as e:
            print(e)

    return render(request, "users/signup.html")


def home(request):
    return render(request, "users/home.html")


def logout(request):
    django_logout(request)
    return redirect("index")


def profile(request):
    user = request.user
    return render(request, "users/profile.html", {"user": user})


def delete_account(request):
    user = request.user
    user.delete()
    return redirect("index")

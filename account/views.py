from django.db import IntegrityError
from django.shortcuts import redirect, render

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages

from .models import CustomUser, ContactMessage

# Create your views here.


def login(request):

    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        email = request.POST.get("email", "")
        password = request.POST.get("floating_password", "")

        if email and password:
            user = authenticate(request, email=email, password=password)

            if user is not None:
                auth_login(request, user)
                return redirect("/")
            else:
                messages.info(request, "Please try again!")

    return render(request, "account/login.html", {"suc": "success"})


def signup(request):

    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        name = request.POST.get("name", "")
        email = request.POST.get("floating_email", "")
        password1 = request.POST.get("floating_password", "")
        password2 = request.POST.get("repeat_password", "")
        company = request.POST.get("floating_company", "")

        if name and email and password1 and password2 and company:

            try:
                user = CustomUser.objects.create_user(email, password1, name, company)

                # Logging the user in right after registration
                user_redirect = authenticate(request, email=email, password=password1)
                auth_login(request, user)

                return redirect("/")

            except IntegrityError:
                messages.error(request, "Email already in use!")

    return render(request, "account/signup.html", {})


@login_required(login_url="/login")
def logout(request):
    auth_logout(request)

    return redirect("/")


@login_required(login_url="/login")
def own_account(request, pk):
    usr = CustomUser.objects.get(pk=pk)
    return render(request, "account/own_account.html", {"user": usr})


@login_required(login_url="/login")
def edit_account(request, pk):
    usr = CustomUser.objects.get(pk=pk)

    if request.method == "POST":
        name = request.POST.get("name", "")
        email = request.POST.get("floating_email", "")
        company = request.POST.get("floating_company", "")

        if name and email and company:
            usr.name = name
            usr.email = email
            usr.company = company
            usr.save()

            return redirect(f"/account/{pk}")

    return render(
        request,
        "account/edit.html",
        {
            "user": usr,
        },
    )


def contact(request):
    if request.method == "POST":
        email = request.POST.get("email", "")
        subject = request.POST.get("subject", "")
        message = request.POST.get("message", "")

        if email and subject and message:
            ContactMessage.objects.create(email=email, subject=subject, message=message)

            return redirect("/")

    return render(request, "account/contact.html", {})

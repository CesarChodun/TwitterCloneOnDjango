import datetime

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import UserData
from .forms import RegisterNewUser, LoginUser

def login_user(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))

    if request.method == "POST":
        form = LoginUser(request.POST)

        if form.is_valid() == False:
            return HttpResponseRedirect(reverse('register'))

        user = authenticate(
            username=form.cleaned_data["login"],
            password=form.cleaned_data["password"])

        if user is not None:
            login(request, user)

            return HttpResponseRedirect(reverse('home'))

        return HttpResponseRedirect(reverse('login'))

    form = LoginUser()

    return render(request , 'userData/login.html', {"form":form})


def logout_user(request):
    logout(request)

    return HttpResponseRedirect(reverse('home'))

def register_user(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))

    if request.method == "POST":
        form = RegisterNewUser(request.POST)

        if form.is_valid() == False:
            return HttpResponseRedirect(reverse('register'))

        user_loggin = form.cleaned_data["login"]
        user_password = form.cleaned_data["password"]

        user = User.objects.create_user(
            user_loggin,
            form.cleaned_data["email"],
            user_password)

        if user is not None:
            user.save()

            data = UserData()
            data.profile = user
            data.registration_date = datetime.datetime.now()
            data.save()

            user_auth = authenticate(
                username=user_loggin,
                password=user_password)

            if user_auth is not None:
                login(request, user)
            else:
                return  HttpResponse("You're not logged in")

            return HttpResponseRedirect(reverse('home'))

        return HttpResponse("You're not logged in")
    else:
        form = RegisterNewUser()

    return render(request , "userData/register.html", {"form":form})

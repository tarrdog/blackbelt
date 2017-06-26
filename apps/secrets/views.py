# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from models import Secrets, Likes
from ..log_reg.models import Users

# Create your views here.
def index(request):

    context = {
     "secrets" : Secrets.objects.recent(10),
     "current_user" : Users.objects.get(id=request.session["current_user"]["id"])
     }

    return render(request, "secrets/index.html", context)

def add_secret(request, user_id, current_page):
    added = Secrets.objects.add_secret(request.POST, user_id)
    if added[0]:
        messages.success(request, added[1])
    else:
        messages.error(request, added[1])

    if current_page == "index":
        return redirect("secrets:index")
    elif current_page == "popular":
        return redirect("secrets:popular")

def add_like(request, user_id, secret_id, current_page):
    Likes.objects.add_like(user_id, secret_id)
    if current_page == "index":
        return redirect("secrets:index")
    elif current_page == "popular":
        return redirect("secrets:popular")

def remove(request, secret_id):

    Secrets.objects.get(id = secret_id).delete()

    return redirect("secrets:index")

def popular(request):

    context = {
     "secrets" : Secrets.objects.popular,
     "current_user" : Users.objects.get(id=request.session["current_user"]["id"])
     }

    return render(request, "secrets/popular.html", context)
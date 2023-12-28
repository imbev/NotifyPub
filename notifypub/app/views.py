from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, "app/index.html")

@login_required(login_url="/login/")
def dashboard(request):
    context = {
        "page_name": "Dashboard"
    }
    return render(request, "app/dashboard.html", context)

def login(request):
    return HttpResponse("Login")

def logout(request):
    return HttpResponse("Logout")

@login_required(login_url="/login/")
def manage_notifications(request):
    context = {
        "page_name": "Manage Notifications"
    }
    return render(request, "app/manage_notifications.html", context)

@login_required(login_url="/login/")
def manage_tokens(request):
    context = {
        "page_name": "Manage Access Tokens"
    }
    return render(request, "app/manage_tokens.html", context)

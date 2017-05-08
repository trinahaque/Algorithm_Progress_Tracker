from django.shortcuts import render, redirect, HttpResponse

def index(request):
    return render(request, "algo_app/index.html")

def register(request):
    return render(request, "algo_app/register.html")

def login(request):
    return render(request, "algo_app/login.html")


def dashboard(request):
    # register = User.objects.register(request.POST)
    return render(request, "algo_app/dashboard.html")


def new(request):
    return render(request, "algo_app/new.html")

def events(request):
    return render(request, "algo_app/events.html")

def resources(request):
    return render(request, "algo_app/resources.html")

def logout(request):
    return redirect("/")

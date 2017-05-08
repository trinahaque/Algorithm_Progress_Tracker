from django.shortcuts import render, HttpResponse

def index(request):
    return render(request, "algo_app/index.html")

def register(request):
    return render(request, "algo_app/register.html")

def login(request):
    return render(request, "algo_app/login.html")

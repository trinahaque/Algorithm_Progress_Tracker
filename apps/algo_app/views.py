from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User, Problem, Type, Source


# log in and registration
def index(request):
    if "first_name" in request.session:
        return redirect('/dashboard')
    return render(request, "algo_app/index.html")


def register(request):
    if "first_name" in request.session:
        return redirect('/dashboard')
    return render(request, "algo_app/register.html")

def registered(request):
    if request.method == "POST":
        result = User.objects.registration(request.POST)
        if result[0] == False:
            for error in result[1]:
                messages.add_message(request, messages.INFO, error)
                return redirect('/register')
        else:
            request.session['first_name']= result[1].first_name
            request.session['id'] = result[1].id
            return redirect('/dashboard')
    return redirect('/')


def login(request):
    if "first_name" in request.session:
        return redirect('/dashboard')
    return render(request, "algo_app/login.html")

def loggedIn(request):
    if request.method == "POST":
        result = User.objects.login(request.POST)
        if result[0] == False:
            for error in result[1]:
                messages.add_message(request, messages.INFO, error)
                return redirect('/login')
        else:
            request.session['first_name']= result[1].first_name
            request.session['id'] = result[1].id
            return redirect('/dashboard')
    return redirect('/')

def logout(request):
    if 'first_name' in request.session:
        request.session.pop('first_name')
        request.session.pop('id')
    return redirect("/")


# pages
def dashboard(request):
    if "id" in request.session:
        return render(request, "algo_app/dashboard.html")
    return redirect('/')

def all(request):
    if "id" in request.session:
        return render(request, "algo_app/all.html")
    return redirect('/')

def new(request):
    if "id" in request.session:
        return render(request, "algo_app/new.html")
    return redirect('/')

def popular(request):
    if "id" in request.session:
        return render(request, "algo_app/popular.html")
    return redirect('/')

def events(request):
    if "id" in request.session:
        return render(request, "algo_app/events.html")
    return redirect('/')

def resources(request):
    if "id" in request.session:
        return render(request, "algo_app/resources.html")
    return redirect('/')


#operation
def add_problem(request):
    if request.method == "POST":
        new_problem = Problem.objects.addProblem(request.POST)

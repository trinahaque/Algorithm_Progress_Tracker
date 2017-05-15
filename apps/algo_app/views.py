from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User, Problem, Type, Source, Event
from django.db.models import Q
import datetime
from datetime import date
from django.utils.timezone import localtime, now
# this imports local time


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
        today = localtime(now()).date()
        start_week = today - datetime.timedelta(days=0)
        end_week = today + datetime.timedelta(days=7)
        events = Event.objects.filter(event_date__range=(start_week, end_week)).order_by('event_date')
        upcoming = Event.objects.filter(Q(event_date__gte=end_week)).order_by('event_date')

        context = {
            "events":events,
            "start_week":start_week,
            "end_week": end_week,
            "upcoming":upcoming
        }
        return render(request, "algo_app/events.html", context)
    return redirect('/')

def event(request, id):
    if "id" in request.session:
        print request.session['id']
        event = Event.objects.filter(user_id=request.session['id'], id=id)
        print event[0]
        context = {
            "event": event[0]
        }
        return render(request, "algo_app/event.html", context)
    # return redirect('/')


def resources(request):
    if "id" in request.session:
        return render(request, "algo_app/resources.html")
    return redirect('/')


#operation
def add_problem(request):
    if request.method == "POST":
        new_problem = Problem.objects.addProblem(request.POST)
    return redirect('/')

def add_event(request):
    if request.method == "POST":
        event = Event.objects.addEvent(request.POST, request.session['id'])
        if event[0] == False:
            for error in event[1]:
                messages.add_message(request, messages.INFO, error)
        return redirect('/events')
    return redirect('/')

from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User, Problem, Type, Event, Solution
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


# rendering pages
def dashboard(request):
    if "id" in request.session:
        today = localtime(now()).date()
        start_week = today - datetime.timedelta(days=0)
        end_week = today + datetime.timedelta(days=7)
        context = {
            "start_week":start_week,
            "end_week": end_week
        }
        return render(request, "algo_app/dashboard.html", context)
    return redirect('/')

def all(request):
    if "id" in request.session:
        array = Problem.objects.filter(prob_type__data_type="array")
        strings = Problem.objects.filter(prob_type__data_type="strings")
        linkedlist = Problem.objects.filter(prob_type__data_type="linkedlist")
        recursion = Problem.objects.filter(prob_type__data_type="recursion")
        sort = Problem.objects.filter(prob_type__data_type="sort")
        heap = Problem.objects.filter(prob_type__data_type="heap")
        bst = Problem.objects.filter(prob_type__data_type="bst")
        hashmap = Problem.objects.filter(prob_type__data_type="hashmap")
        graph = Problem.objects.filter(prob_type__data_type="graph")

        context = {
            "array":array,
            "strings": strings,
            "linkedlist": linkedlist,
            "recursion": recursion,
            "sort": sort,
            "heap": heap,
            "bst": bst,
            "hashmap": hashmap,
            "graph": graph
        }
        return render(request, "algo_app/all.html", context)
    return redirect('/')

def new(request):
    if "id" in request.session:
        return render(request, "algo_app/new.html")
    return redirect('/')

def popular(request):
    if "id" in request.session:
        popular = Problem.objects.filter(prob_popular=True)
        for problem in popular:
            print problem.prob_name
        context = {
         "popular": popular
        }
        return render(request, "algo_app/popular.html", context)
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
        event = Event.objects.filter(user_id=request.session['id'], id=id)
        context = {
            "event": event[0]
        }
        return render(request, "algo_app/event.html", context)
    # return redirect('/')

def resources(request):
    if "id" in request.session:
        return render(request, "algo_app/resources.html")
    return redirect('/')


#CRUD Problems
def add_problem(request):
    if request.method == "POST":
        new_problem = Problem.objects.addProblem(request.POST, request.session['id'])
        if new_problem[0] == False:
            for error in new_problem[1]:
                messages.add_message(request, messages.INFO, error)
                return redirect('/new')
        else:
            return redirect('problem', id=new_problem[1].id)
    return redirect('/')

def delete_problem(request, id):
    if "id" in request.session:
        user = User.objects.get(id=request.session['id'])
        Problem.objects.get(id=id).delete()
        return redirect('/all')
    return redirect('/')

def problem(request, id):
    if "id" in request.session:
        problem = Problem.objects.get(id=id)
        user = User.objects.get(id=request.session['id'])
        solutions = Solution.objects.filter(user=user, problem=problem)

        context = {
            "problem":problem,
            "solutions":solutions
        }
        return render(request, "algo_app/problem.html", context)
    return redirect('/')


def add_solution(request, pid):
    if "id" in request.session:
        solution = Solution.objects.addSolution(request.POST, request.session['id'], pid)
        if solution[0] == False:
            for error in solution[1]:
                messages.add_message(request, messages.INFO, error)
        return redirect('problem', id=pid)
    return redirect('/')

def delete_solution(request, sid, pid):
    if "id" in request.session:
        Solution.objects.get(id=sid).delete()
        return redirect('problem', id=pid)
    return redirect('/')



# CRUD Event
def add_event(request):
    if request.method == "POST":
        event = Event.objects.addEvent(request.POST, request.session['id'])
        if event[0] == False:
            for error in event[1]:
                messages.add_message(request, messages.INFO, error)
        return redirect('/events')
    return redirect('/')

def delete_event(request, id):
    if "id" in request.session:
        Event.objects.get(id=id, user_id=request.session['id']).delete()
        return redirect('/events')
    return redirect('/')

def update_event(request, id):
    if "id" in request.session:
        update_event = Event.objects.update_event(request.POST, request.session['id'], id)
        if update_event[0] == False:
            for error in update_event[1]:
                messages.add_message(request, messages.INFO, error)
                return redirect('edit_event', id=id)
        else:
            return redirect("/events")

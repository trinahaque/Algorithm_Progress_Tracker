from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User, Problem, Type, Event, Solution, Calendar
from django.db.models import Q
import datetime
from datetime import date
from django.utils.timezone import localtime, now
# this imports local time


def daterange(start_date, end_date):
    for n in range(int((end_date-start_date).days)):
        yield start_date + datetime.timedelta(n)


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
        user = User.objects.get(id=request.session['id'])
        today = localtime(now()).date()
        start_date = today - datetime.timedelta(days=0)
        end_date = today + datetime.timedelta(days=7)
        dateranges = daterange(start_date, end_date)

        calendars = Calendar.objects.filter(date__range=(start_date, end_date), user=user).order_by('date')
        prob_ids = [calendar.problem.id for calendar in calendars]
        problems = Problem.objects.filter(user=user).exclude(id__in=prob_ids)

        context = {
            "start_date":start_date,
            "end_date": end_date,
            "problems": problems,
            "dateranges": dateranges,
            "calendars": calendars
        }
        return render(request, "algo_app/dashboard.html", context)
    return redirect('/')

def all(request):
    if "id" in request.session:
        array = Problem.objects.filter(prob_type__data_type="array", user_id=request.session['id'])
        strings = Problem.objects.filter(prob_type__data_type="strings", user_id=request.session['id'])
        linkedlist = Problem.objects.filter(prob_type__data_type="linkedlist", user_id=request.session['id'])
        recursion = Problem.objects.filter(prob_type__data_type="recursion", user_id=request.session['id'])
        sort = Problem.objects.filter(prob_type__data_type="sort", user_id=request.session['id'])
        heap = Problem.objects.filter(prob_type__data_type="heap", user_id=request.session['id'])
        bst = Problem.objects.filter(prob_type__data_type="bst", user_id=request.session['id'])
        hashmap = Problem.objects.filter(prob_type__data_type="hashmap", user_id=request.session['id'])
        graph = Problem.objects.filter(prob_type__data_type="graph", user_id=request.session['id'])

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
        user = User.objects.get(id=request.session['id'])
        popular = Problem.objects.filter(prob_popular=True, user=user)

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

def event(request, eid):
    if "id" in request.session:
        event = Event.objects.filter(user_id=request.session['id'], id=eid)
        context = {
            "event": event[0]
        }
        return render(request, "algo_app/event.html", context)
    return redirect('/')

def resources(request):
    if "id" in request.session:
        return render(request, "algo_app/resources.html")
    return redirect('/')


#CRUD Problems
def add_problem(request):
    if request.method == "POST" and "id" in request.session:
        new_problem = Problem.objects.addProblem(request.POST, request.session['id'])
        if new_problem[0] == False:
            for error in new_problem[1]:
                messages.add_message(request, messages.INFO, error)
                return redirect('/new')
        else:
            return redirect('problem', id=new_problem[1].id)
    return redirect('/')

def delete_problem(request, pid):
    if "id" in request.session:
        user = User.objects.get(id=request.session['id'])
        Problem.objects.get(id=pid).delete()
        return redirect('/all')
    return redirect('/')

def problem(request, pid):
    if "id" in request.session:
        problem = Problem.objects.get(id=pid)
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
        return redirect('problem', pid=pid)
    return redirect('/')

def delete_solution(request, sid, pid):
    if "id" in request.session:
        Solution.objects.get(id=sid).delete()
        return redirect('problem', pid=pid)
    return redirect('/')



# CRUD Event
def add_event(request):
    if request.method == "POST" and "id" in request.session:
        event = Event.objects.addEvent(request.POST, request.session['id'])
        if event[0] == False:
            for error in event[1]:
                messages.add_message(request, messages.INFO, error)
        return redirect('/events')
    return redirect('/')

def delete_event(request, eid):
    if "id" in request.session:
        Event.objects.get(id=eid, user_id=request.session['id']).delete()
        return redirect('/events')
    return redirect('/')

def update_event(request, eid):
    if "id" in request.session:
        update_event = Event.objects.update_event(request.POST, request.session['id'], eid)
        if update_event[0] == False:
            for error in update_event[1]:
                messages.add_message(request, messages.INFO, error)
                return redirect('edit_event', id=eid)
        else:
            return redirect("/events")


#Calendar/Dashboard
def add_calendar(request):
    if request.method == "POST" and "id" in request.session:
        calendar = Calendar.objects.addCalendar(request.POST, request.session['id'])
        if calendar[0] == False:
            for error in calendar[1]:
                messages.add_message(request, messages.INFO, error)
        return redirect("/dashboard")
    return redirect('/')

from django.shortcuts import render, HttpResponse

def index(request):
    response = "Just created a new app after a long time"
    return HttpResponse(response)

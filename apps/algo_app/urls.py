from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^registered$', views.registered),
    url(r'^login$', views.login),
    url(r'^loggedIn$', views.loggedIn),
    url(r'^logout$', views.logout),
    url(r'^dashboard$', views.dashboard),
    url(r'^all$', views.all),
    url(r'^new$', views.new),

    url(r'^add_problem$', views.add_problem),
    url(r'^problem/(?P<id>\d+)$', views.problem, name="problem"),
    url(r'^delete/(?P<id>\d+)$', views.delete_problem),

    url(r'^add_solution/(?P<pid>\d+)$', views.add_solution),
    url(r'^delete_solution/(?P<sid>\d+)/(?P<pid>\d+)$', views.delete_solution),

    url(r'^popular$', views.popular),
    url(r'^events$', views.events),
    url(r'^edit/(?P<id>\d+)$', views.event, name="edit_event"),
    url(r'^delete_event/(?P<id>\d+)$', views.delete_event),
    url(r'^update_event/(?P<id>\d+)$', views.update_event),
    url(r'^add_event$', views.add_event),
    url(r'^resources$', views.resources),

    url(r'^add_calendar$', views.add_calendar),
]

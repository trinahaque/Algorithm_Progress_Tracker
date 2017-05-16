from __future__ import unicode_literals
from django.db import models
import re, bcrypt
from datetime import datetime, date
Email_Regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'/^[a-zA-Z]+', re.MULTILINE)
PASSWORD_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*(_|[^\w])).+$', re.MULTILINE)

class UserManager(models.Manager):

    def registration(self, POST):
        first_name = POST['first_name'].lower()
        last_name = POST['last_name'].lower()
        email = POST['email'].lower()
        password = POST['password']

        errors = []

        valid = True
        if len(email) < 1 or len(first_name) < 1 or len(last_name) < 1 or len(password) < 1:
            errors.append("A field can not be empty")
            valid = False
        else:
            # names
            if len(first_name) < 2 or len(last_name) < 2:
                errors.append("Name field needs at least two characters")
                valid = False
            elif first_name.isalpha() == False or last_name.isalpha() == False:
                errors.append("Name field needs to be all letters")
                valid = False


            # email
            if not Email_Regex.match(email):
                errors.append("Field required in email format")
                valid = False

            # password
            if len(password) < 8:
                errors.append("Password needs at least 8 characters")
                valid = False

            if not PASSWORD_REGEX.match(password):
                errors.append('Password Requires atleast One Uppercase, One Lowercase, One Number and One Symbol')
                valid = False

        if valid:
            distinct_list = User.objects.filter(email = email)
            if not distinct_list:
                pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
                user = User.objects.create(first_name=first_name, last_name=last_name, email=email, password=pw_hash)
                return (True, user)
            else:
                # valid_messages.append("Email already exists")
                errors.append("Email already exists")

        return (False, errors)


    def login(self, POST):

        email = POST['email'].lower()
        password = POST['password']

        login_messages = []

        if len(email) < 1 or len(password) < 1:
            login_messages.append("A field can not be empty")

        if not Email_Regex.match(email):
            login_messages.append("Field required in email format")

        if len(password) < 8:
            login_messages.append("Password needs at least 8 characters")

        if len(login_messages) < 1:
            user = User.objects.filter(email=email)
            # print user
            if len(user) > 0:
                if bcrypt.hashpw(password.encode(), user[0].password.encode()) == user[0].password.encode():
                    return True, user[0]
                else:
                    login_messages.append("Wrong password")
            else:
                login_messages.append("Not a registered user")

        return False, login_messages


class ProblemManager(models.Manager):
    def addProblem(self, POST):
        prob_type = POST['prob_type']
        prob_name = POST['prob_name'].lower()
        prob_statement = POST['prob_statement']
        # prob_statement = POST.get('prob_statement')
        prob_support = POST['prob_support']
        # prob_comment = POST.get('comment')
        prob_sources = POST['prob_sources']
        # print prob_sources

        data_type = Type.objects.get(data_type=prob_type)


class EventManager(models.Manager):
    def addEvent(self, POST, id):
        event_name = POST['event_name'].lower()
        event_date = POST['event_date']
        event_time = POST['event_time']
        event_location = POST['event_location'].lower()
        event_comment = POST['event_comment']
        errors = []

        valid = True
        if len(event_name) < 1 or len(event_date) < 1 or len(event_time) < 1 or len(event_location) < 1 or len(event_comment) < 1:
            errors.append("A field can not be empty")
            valid = False

        if event_date < unicode(datetime.today().date()):
            errors.append("Can not add past events")
            valid = False

        if valid:
            user = User.objects.get(id=id)
            event = Event.objects.create(user=user, event_name=event_name, event_date=event_date, event_time=event_time, event_location=event_location, event_comment=event_comment)
            return (True, event)
        return (False, errors)

    def update_event(self, POST, user_id, event_id):
        event_name = POST['event_name']
        event_date = POST['event_date']
        event_time = POST['event_time']
        event_location = POST['event_location']
        event_comment = POST['event_comment']
        errors = []

        valid = True
        if len(event_name) < 1 or len(event_date) < 1 or len(event_location) < 1 or len(event_time) < 1 or len(event_comment) < 1:
            errors.append("A field can not be empty")
            valid = False

        if event_date < unicode(datetime.today().date()):
            errors.append('A date can not be in the past')
            valid = False

        if valid:
            updated_event = Event.objects.filter(id=event_id, user_id=user_id).update(event_name=event_name, event_date = event_date, event_time=event_time, event_location=event_location, event_comment=event_comment)
            return (True, updated_event)

        return (False, errors)


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Type(models.Model):
    data_type = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)


class Source(models.Model):
    prob_source = models.CharField(max_length=255)
    # created_at = models.DateTimeField(auto_now_add = True)
    # updated_at = models.DateTimeField(auto_now=True)


class Problem(models.Model):
    prob_type = models.ForeignKey(Type)
    prob_name = models.TextField(max_length=1000)
    prob_statement = models.TextField(max_length=1000)
    prob_support = models.TextField(max_length=1000)
    prob_popular = models.BooleanField(default=False)
    prob_comment = models.TextField(max_length=1000)
    prob_sources = models.ManyToManyField(Source)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ProblemManager()


class Event(models.Model):
    user = models.ForeignKey(User)
    event_name = models.CharField(max_length=255)
    event_date = models.CharField(max_length=255)
    event_time = models.CharField(max_length=255)
    event_location = models.TextField(max_length=1000)
    event_comment = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = EventManager()

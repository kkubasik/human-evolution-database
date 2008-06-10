from google.appengine.ext.db import djangoforms
from google.appengine.api import mail
from google.appengine.api import users
from google.appengine.api import urlfetch
from google.appengine.ext import db


from django import newforms as forms
from django.http import HttpResponse, HttpResponseRedirect
from django.http import HttpResponseForbidden, HttpResponseNotFound
from django.shortcuts import render_to_response
import django.template
from django.utils import simplejson

from models import Fossil




def user_stuff(request):
    if request.user:
        login = users.create_logout_url(request.path)
        login_linktext = 'Logout'
    else:
        login = users.create_login_url(request.path)
        login_linktext = 'Login'
    return login_linktext, login

def index(request):
    fossils_query = Fossil.all().order('-date')
    fossils = fossils_query.fetch(10)

    login_linktext, login = user_stuff(request)

    template_values = {
      'fossils': fossils,
      'login': login,
      'login_linktext': login_linktext,
      }
    return render_to_response('index.html',template_values)

def show(request,slug):
    
    fossils_query = Fossil.all().filter('slug =', slug)
    fossils = fossils_query.fetch(1)
    
    login_linktext, login = user_stuff(request)
        
    template_values = {
        'fossils': fossils,
        'login': login,
        'login_linktext': login_linktext,
        }
    
    return render_to_response("fossil.html",template_values)
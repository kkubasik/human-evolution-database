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
import logging
from models import Fossil

class FossilForm(forms.Form):
    title = forms.CharField(max_length=100,
                            widget=forms.TextInput(attrs={'size': 60}))
    slug = forms.CharField(max_length=100,
                            widget=forms.TextInput(attrs={'size': 60}))
    antiquity = forms.CharField(max_length=100,
                            widget=forms.TextInput(attrs={'size': 60}))
    species = forms.CharField(max_length=100,
                            widget=forms.TextInput(attrs={'size': 60}))
    field_site = forms.CharField(max_length=100,
                            widget=forms.TextInput(attrs={'size': 60}))
    lat = forms.CharField(max_length=100,
                            widget=forms.TextInput(attrs={'size': 60}))
    long = forms.CharField(max_length=100,
                            widget=forms.TextInput(attrs={'size': 60}))
    doi = forms.CharField(max_length=100,
                            widget=forms.TextInput(attrs={'size': 60}))
    
    image = forms.ImageField()
    
    

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

def new(request):
    if request.method == "POST":
        logging.log(logging.WARN, "Cannot Save Data Yet")
        return HttpResponse(content="No Response Yet")
    login_linktext, login = user_stuff(request)
    fossil_form = FossilForm()
    template_values = {
      'login': login,
      'login_linktext': login_linktext,
      'fossil_form': fossil_form,
      }
    return render_to_response('new.html',template_values)
    
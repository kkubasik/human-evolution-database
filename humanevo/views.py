from google.appengine.ext.db import djangoforms
from google.appengine.api import mail
from google.appengine.api import users
from google.appengine.api import urlfetch
from google.appengine.ext import db
from google.appengine.api import images

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
    
    image = forms.FileField()
    
class ContactForm(forms.Form):
    sender = forms.EmailField()
    subject = forms.CharField(max_length=100)
    message = forms.CharField()
    cc_myself = forms.BooleanField(required=False)

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

#def new(request):
#    if request.method == "POST":
#        logging.log(logging.WARN, "Cannot Save Data Yet")
#        return HttpResponse(content="No Response Yet")
#    login_linktext, login = user_stuff(request)
#    fossil_form = FossilForm()
#    template_values = {
#      'login': login,
#      'login_linktext': login_linktext,
#      'fossil_form': fossil_form,
#      }
#    return render_to_response('new.html',template_values)
    
    
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Do form processing here...
            return HttpResponseRedirect('/url/on_success/')
    else:
        form = ContactForm()

    return render_to_response('contact.html', {'form': form})


def new(request):
    if request.method == 'POST':
        form = FossilForm(request.POST, request.FILES)
        if form.is_valid():
            logging.log(logging.DEBUG, form.cleaned_data)
            f= Fossil()
            f.author = request.user
            f.title = form.cleaned_data['title']
            f.slug = form.cleaned_data['slug']
            f.species = form.cleaned_data['species']
            f.antiquity = form.cleaned_data['antiquity']
            f.doi = form.cleaned_data['doi']
            f.loc = db.GeoPt(lat=form.cleaned_data['lat'],lon=form.cleaned_data['long'])
            f.field_site = form.cleaned_data['field_site']
            i = images.Image(form.cleaned_data['image'].content)
            f.image = i.execute_transforms()
            f.populate_doi(f.doi)
            # Do form processing here...
            return HttpResponseRedirect('/')
    else:
        form = FossilForm()

    return render_to_response('new.html', {'form': form})


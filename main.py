import cgi, os, re
import os
import wsgiref.handlers
import re

from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.api import urlfetch
from django.utils import simplejson
from xml.dom import minidom

class Fossil(db.Model):
  author = db.UserProperty()
  date = db.DateTimeProperty(auto_now_add=True)
  title = db.StringProperty(multiline=False)
  antiquity = db.StringProperty(multiline=False)
  species = db.StringProperty(multiline=False)
  field_site = db.StringProperty(multiline=False)
  lat = db.StringProperty(multiline=False)
  lng = db.StringProperty(multiline=False)
  doi = db.StringProperty(multiline=False)

class MainPage(webapp.RequestHandler):
  def get(self):
    fossils_query = Fossil.all().order('-date')
    fossils = fossils_query.fetch(10)

    if users.get_current_user():
      login = users.create_logout_url(self.request.uri)
      login_linktext = 'Logout'
    else:
      login = users.create_login_url(self.request.uri)
      login_linktext = 'Login'

    template_values = {
      'fossils': fossils,
      'login': login,
      'login_linktext': login_linktext,
      }

    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path, template_values))

class IndividualFossil(webapp.RequestHandler):
  def get(self, title):
	fossil = re.search('^/fossil/(.*)$', self.request.path).group(1) 
	# fossil = '/'.join(self.request.path.split('/')[1:])
	fossils_query = Fossil.all().filter('title =', fossil)
	fossils = fossils_query.fetch(1)
	
	if users.get_current_user():
		login = users.create_logout_url(self.request.uri)
		login_linktext = 'Logout'
	else:
		login = users.create_login_url(self.request.uri)
		login_linktext = 'Login'
		
	template_values = {
		'fossils': fossils,
		'login': login,
		'login_linktext': login_linktext,
		}
	
	path = os.path.join(os.path.dirname(__file__), 'fossil.html')
	self.response.out.write(template.render(path, template_values))
	
class SpeciesList(webapp.RequestHandler):
  def get(self, species):
	fossil = re.search('^/species/(.*)$', self.request.path).group(1) 
	fossils_query = Fossil.all().filter('species =', fossil)
	fossils = fossils_query.fetch(100)

	if users.get_current_user():
		login = users.create_logout_url(self.request.uri)
		login_linktext = 'Logout'
	else:
		login = users.create_login_url(self.request.uri)
		login_linktext = 'Login'

	template_values = {
		'fossils': fossils,
		'login': login,
		'login_linktext': login_linktext,
		}

	path = os.path.join(os.path.dirname(__file__), 'species.html')
	self.response.out.write(template.render(path, template_values))

class Map(webapp.RequestHandler):
  def get(self):
    fossils_query = Fossil.all().order('-date')
    fossils = fossils_query.fetch(100)

    if users.get_current_user():
      login = users.create_logout_url(self.request.uri)
      login_linktext = 'Logout'
    else:
      login = users.create_login_url(self.request.uri)
      login_linktext = 'Login'

    template_values = {
      'fossils': fossils,
      'login': login,
      'login_linktext': login_linktext,
      }

    path = os.path.join(os.path.dirname(__file__), 'map.html')
    self.response.out.write(template.render(path, template_values))

class Submission(webapp.RequestHandler):
  def get(self):
	fossils_query = Fossil.all().order('-date')
	fossils = fossils_query.fetch(10)
	
	if users.get_current_user():
	  login = users.create_logout_url(self.request.uri)
	  login_linktext = 'Logout'
	else:
	  login = users.create_login_url(self.request.uri)
	  login_linktext = 'Login'
	
	template_values = {
	  'fossils': fossils,
	  'login': login,
	  'login_linktext': login_linktext,
	  }
	
	path = os.path.join(os.path.dirname(__file__), 'submit.html')
	self.response.out.write(template.render(path, template_values))

class Records(webapp.RequestHandler):
	def post(self):
		fossil = Fossil()
		
		if users.get_current_user():
			fossil.author = users.get_current_user()
			
		fossil.title = self.request.get('title')
		fossil.species = self.request.get('species')
		fossil.antiquity = self.request.get('antiquity')
		fossil.field_site = self.request.get('field_site')
		fossil.lat = self.request.get('lat')
		fossil.lng = self.request.get('lng')
		fossil.doi = self.request.get('doi')
		fossil.put()
		self.redirect('/')		

def main():
  application = webapp.WSGIApplication(
                                       [('/', MainPage),
										('/submit', Submission),
										('/map', Map),
										(r'/fossil/(.*)', IndividualFossil),
										(r'/species/(.*)', SpeciesList),
                                        ('/submitted', Records)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
  main()
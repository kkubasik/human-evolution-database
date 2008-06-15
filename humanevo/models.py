# Python imports
import logging

# AppEngine imports
from google.appengine.api import users, urlfetch
from google.appengine.ext import db, search
import urllib
from xml.dom import minidom
from django import newforms as forms
from django.newforms.util import ErrorList



class Fossil(search.SearchableModel):
    author = db.UserProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    title = db.StringProperty()
    slug = db.StringProperty()
    antiquity = db.StringProperty()
    species = db.StringProperty()
    field_site = db.StringProperty()
    loc = db.GeoPtProperty()
    doi = db.StringProperty()
    doi_title= db.StringProperty()
    doi_authors = db.StringListProperty()
    doi_abstract = db.TextProperty()
    image_path = db.StringProperty()
    
    
    
    def populate_doi(self,query, email='simon@simon.net.nz', tool='SimonsPythonQuery', database='pubmed'):
        params = {
            'db':database,
            'tool':tool,
            'email':email,
            'term':query,
            'usehistory':'y',
            'retmax':1
        }
        # try to resolve the PubMed ID of the DOI
        url = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?' + urllib.urlencode(params)
        data = urlfetch.fetch(url).content
    
        # parse XML output from PubMed...
        xmldoc = minidom.parseString(data)
        ids = xmldoc.getElementsByTagName('Id')
    
        # nothing found, exit
        if len(ids) == 0:
            raise ValueError, "DoiNotFound"
    
        # get ID
        id = ids[0].childNodes[0].data
    
        # remove unwanted parameters
        params.pop('term')
        params.pop('usehistory')
        params.pop('retmax')
        # and add new ones...
        params['id'] = id
        
        params['retmode'] = 'xml'
    
        # get citation info:
        url = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?' + urllib.urlencode(params)
        data = urlfetch.fetch(url).content
        
        xmldoc = minidom.parseString(data)

        title = xmldoc.getElementsByTagName('ArticleTitle')[0]
        title = title.childNodes[0].data
        
        abstract = xmldoc.getElementsByTagName('AbstractText')[0]
        abstract = abstract.childNodes[0].data
        
        authors = xmldoc.getElementsByTagName('AuthorList')[0]
        authors = authors.getElementsByTagName('Author')
        authorlist = []
        for author in authors:
            LastName = author.getElementsByTagName('LastName')[0].childNodes[0].data
            Initials = author.getElementsByTagName('Initials')[0].childNodes[0].data
            author = '%s, %s' % (LastName, Initials)
            authorlist.append(author)
            
        self.doi_abstract = abstract
        self.doi_title = title
        self.doi_authors = authorlist
        self.save()
        
        



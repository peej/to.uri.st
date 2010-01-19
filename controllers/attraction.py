from google.appengine.ext import webapp
import os
from google.appengine.ext.webapp import template
from google.appengine.ext import db

from models.attraction import Attraction

class AttractionPage(webapp.RequestHandler):
    def get(self, attractionId):
        
        attraction = Attraction.all()
        attraction.filter("id =", attractionId)
        
        template_values = {
            'attraction': attraction.get()
        }
        
        path = os.path.join(os.path.dirname(__file__), '../templates/attraction.html')
        
        self.response.headers.add_header('Content-type', 'text/html')
        
        self.response.out.write(template.render(path, template_values))
        

from google.appengine.ext import webapp
import os
from google.appengine.ext.webapp import template
from google.appengine.ext import db

from models.attraction import Attraction

class HomePage(webapp.RequestHandler):
    def get(self):
        
        recent = Attraction.all()
        recent.filter("visible =", True)
        recent.order("-modified")
        
        popular = Attraction.all()
        popular.filter("visible =", True)
        popular.order("rating")
        
        template_values = {
            'recent': recent.fetch(5),
            'popular': popular.fetch(5)
        }
        
        path = os.path.join(os.path.dirname(__file__), '../templates/home.html')
        
        self.response.headers.add_header('Content-type', 'text/html')
        
        self.response.out.write(template.render(path, template_values))
        

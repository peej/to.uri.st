from google.appengine.ext import db

from controllers.controller import Controller
from models.attraction import Attraction

class HomePage(Controller):
    def get(self):
        
        recent = Attraction.all()
        recent.filter("next =", None)
        recent.order("-datetime")
        
        popular = Attraction.all()
        popular.filter("next =", None)
        popular.order("rating")
        
        template_values = {
            'recent': recent.fetch(5),
            'popular': popular.fetch(5)
        }
        
        self.output('home.html', template_values)
        

from google.appengine.ext import db

from controllers.controller import Controller
from models.attraction import Attraction

class AttractionPage(Controller):
    def get(self, attractionId):
        
        attraction = Attraction.all()
        attraction.filter("id =", attractionId)
        
        template_values = {
            'attraction': attraction.get()
        }
        
        self.output('attraction.html', template_values)
        

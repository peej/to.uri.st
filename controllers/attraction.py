from google.appengine.ext import db

from controllers.controller import Controller
from models.attraction import Attraction

class AttractionPage(Controller):
    def get(self, attractionId):
        
        attractions = Attraction.all()
        attractions.filter("id =", attractionId)
        attraction = attractions.get()
        
        attraction.picture = attraction.picture.replace('.jpg', '_m.jpg')
        
        template_values = {
            'attraction': attraction
        }
        
        self.output('attraction.html', template_values)
        

from google.appengine.ext import db

from controllers.controller import Controller
from models.attraction import Attraction

class AttractionPage(Controller):
    def get(self, attractionId):
        
        attractions = Attraction.all()
        attractions.filter("id =", attractionId)
        attraction = attractions.get()
        
        attraction.picture = self.convertFlickrUrl(attraction.picture, 'm')
        
        template_values = {
            'attraction': attraction
        }
        
        self.output('attraction', 'html', template_values)
        

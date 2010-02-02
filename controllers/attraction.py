from google.appengine.ext import db

from controllers.controller import Controller
from models.attraction import Attraction

class AttractionPage(Controller):
    def get(self, attractionId):
        
        attractions = Attraction.all()
        attractions.filter("id =", attractionId)
        attraction = attractions.get()
        
        if attraction:
            attraction.picture = self.convertFlickrUrl(attraction.picture, 'm')
            
            template_values = {
                'attraction': attraction
            }
            
            self.output('attraction', 'html', template_values)
        else:
            self.output('404', 'html')

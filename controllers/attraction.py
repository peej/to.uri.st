from google.appengine.ext import db

from controllers.controller import Controller
from models.attraction import Attraction

class AttractionPage(Controller):
    def get(self, attractionId, type):
        
        attractions = Attraction.all()
        attractions.filter("id =", attractionId)
        attraction = attractions.get()
        
        if attraction:
            attraction.picture = self.convertFlickrUrl(attraction.picture, 'm')
            
            if attraction.user:
                attraction.userid = self.getUserId(attraction.user)
                attraction.nickname = attraction.user.nickname()
            
            template_values = {
                'attraction': attraction,
                'gpx': self.request.url.replace('.html', '.gpx')
            }
            
            self.output('attraction', type, template_values)
        else:
            self.output('404', 'html')

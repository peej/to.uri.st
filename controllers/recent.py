from google.appengine.ext import db

from controllers.controller import Controller
from models.attraction import Attraction

class RecentPage(Controller):
    
    def get(self):
        
        page = int(self.request.get("page", 1));
        
        recent = Attraction.all()
        recent.filter("next =", None)
        recent.order("-datetime")
        
        attractions = recent.fetch(26, (page - 1) * 26)
        
        numberOfAttractions = len(attractions)
        attractionCount = 64
        for attraction in attractions:
            attractionCount = attractionCount + 1
            if attractionCount < 91:
                attraction.label = chr(attractionCount)
        
        template_values = {
            'attractions': attractions,
            'nextpage': page + 1
        }
        
        self.output('recent', 'html', template_values)
        

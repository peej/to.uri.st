from google.appengine.ext import db

from controllers.controller import Controller
from models.attraction import Attraction

class HistoryPage(Controller):
    def get(self, attractionId):
        
        attractions = []
        
        while attractionId:
            query = Attraction.all()
            query.filter("id =", attractionId)
            attraction = query.get()
            attractions.append(attraction)
            attractionId = attraction.previous if attraction.previous else False
        
        template_values = {
            'name': attraction.name,
            'attractions': attractions
        }
        
        self.output('history.html', template_values)
        

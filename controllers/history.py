from google.appengine.ext import db
import difflib

from controllers.controller import Controller
from models.attraction import Attraction

class HistoryPage(Controller):
    def get(self, attractionId):
        
        attractions = []
        
        query = Attraction.all()
        query.filter("id =", attractionId)
        attraction = query.get()
        
        while attraction.next != None:
            query = Attraction.all()
            query.filter("id =", attraction.next)
            attraction = query.get()
            attractions.insert(0, attraction)
        
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
        

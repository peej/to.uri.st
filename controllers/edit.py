from google.appengine.ext import db

from controllers.controller import Controller
from models.attraction import Attraction

class EditPage(Controller):
    
    def get(self, attractionId):
        
        query = Attraction.all()
        query.filter("id =", attractionId)
        attraction = query.get()
        
        template_values = {
            'attraction': attraction
        }
        
        self.output('edit.html', template_values)
    
    
    def post(self, attractionId):
        
        attraction = {}
        attraction['id'] = attractionId
        attraction['name'] = self.request.get('name')
        attraction['region'] = self.request.get('region')
        attraction['description'] = self.request.get('description')
        attraction['location'] = {}
        attraction['location']['lat'] = self.request.get('lat')
        attraction['location']['lon'] = self.request.get('lon')
        attraction['href'] = self.request.get('href')
        attraction['picture'] = self.request.get('picture')
        
        if self.request.get('location.x') and self.request.get('location.y'):
            attraction['location']['lat'] = float(attraction['location']['lat']) - ((float(self.request.get('location.y')) - 75) / 18000) + 0.001
            attraction['location']['lon'] = float(attraction['location']['lon']) + ((float(self.request.get('location.x')) - 150) / 12000)
        
        template_values = {
            'attraction': attraction
        }
        
        self.output('edit.html', template_values)
        

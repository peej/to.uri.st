from google.appengine.ext import db
import re, md5

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
        
        errors = {}
        
        if len(attraction['name']) == 0:
            errors['name'] = True
            errors['name_empty'] = True
        if len(attraction['name']) > 100:
            errors['name'] = True
            errors['name_long'] = True
        
        if len(attraction['region']) > 100:
            errors['region'] = True
        
        if float(attraction['location']['lat']) < -90 or float(attraction['location']['lat']) > 90:
            errors['location'] = True
        
        if float(attraction['location']['lon']) < -180 or float(attraction['location']['lon']) > 180:
            errors['location'] = True
        
        if not len(attraction['href']) == 0 and not re.match(r"^https?://.+$", attraction['href']):
            errors['href'] = True
        
        if not len(attraction['picture']) == 0 and not re.match(r"^https?://.+$", attraction['href']):
            errors['picture'] = True
        
        if errors:
            
            template_values = {
                'attraction': attraction,
                'errors': errors
            }
            
            self.output('edit.html', template_values)
            
        else:
            
            next = attractionId
            while next:
                query = Attraction.all()
                query.filter("id =", next)
                latestAttraction = query.get()
                next = latestAttraction.next
            
            try:
                newId = db.run_in_transaction(self.saveAttraction, latestAttraction.key(), attraction)
                self.redirect('/attractions/' + newId + '.html')
                
            except db.Error:
                
                template_values = {
                    'attraction': attraction,
                    'errors': {
                        'save': True
                    }
                }
                self.output('edit.html', template_values)
                
    
    def saveAttraction(self, key, attractionData):
        
        oldAttraction = db.get(key)
        
        newId = md5.new(unicode(attractionData)).hexdigest()
        
        oldAttraction.next = newId
        
        newAttraction = Attraction(
            parent = oldAttraction,
            id = newId,
            previous = oldAttraction.id,
            name = attractionData['name'],
            region = attractionData['region'],
            description = attractionData['description'],
            location = db.GeoPt(
                lat = attractionData['location']['lat'],
                lon = attractionData['location']['lon']
            ),
            href = attractionData['href'],
            picture = attractionData['picture'],
            free = oldAttraction.free,
            rating = oldAttraction.rating,
            user = None
        )
        
        oldAttraction.put()
        newAttraction.put()
        
        return newId

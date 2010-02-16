from google.appengine.ext import db
import re

from controllers.controller import Controller
from models.attraction import Attraction

class EditPage(Controller):
    
    def get(self, attractionId):
        
        query = Attraction.all()
        query.filter("id =", attractionId)
        attraction = query.get()
        
        attraction.picture = self.convertFlickrUrl(attraction.picture, 'm')
        
        template_values = {
            'attraction': attraction
        }
        
        self.output('edit', 'html', template_values)
    
    
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
        attraction['tags'] = self.request.get('tags').split(' ')
        
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
        
        if not attraction['location']['lat'] or float(attraction['location']['lat']) < -90 or float(attraction['location']['lat']) > 90:
            errors['location'] = True
        
        if not attraction['location']['lon'] or float(attraction['location']['lon']) < -180 or float(attraction['location']['lon']) > 180:
            errors['location'] = True
        
        if not len(attraction['href']) == 0 and not re.match(r"^https?://.+$", attraction['href']):
            errors['href'] = True
        
        if not len(attraction['picture']) == 0 and not re.match(r"^https?://.+$", attraction['picture']):
            errors['picture'] = True
        
        for tag in attraction['tags']:
            if not re.match(r"^[a-z0-9]+$", tag):
                errors['tags'] = True
        
        if errors or (self.request.get('location.x') and self.request.get('location.y')):
            
            attraction['picture'] = self.convertFlickrUrl(attraction['picture'], 'm')
            
            template_values = {
                'attraction': attraction,
                'errors': errors
            }
            
            self.output('edit', 'html', template_values)
            
        else:
            
            next = attractionId
            while next: # walk to newest version of this attraction
                query = Attraction.all()
                query.filter("id =", next)
                latestAttraction = query.get()
                next = latestAttraction.next
            
            try:
                newId = self.saveAttraction(latestAttraction, attraction)
                
                from google.appengine.api import users
                self.getUserObject(users.get_current_user()) # create user object if it doesn't exist
                
                self.redirect('/attractions/' + newId + '.html')
                
                return
                
            except:
                
                template_values = {
                    'attraction': attraction,
                    'errors': {
                        'save': True
                    }
                }
                self.output('edit', 'html', template_values)
    
    def saveAttraction(self, latestAttraction, attraction):
        
        oldGeoBoxId = self.calcGeoBoxId(latestAttraction.location.lat, latestAttraction.location.lon)
        newGeoBoxId = self.calcGeoBoxId(attraction['location']['lat'], attraction['location']['lon'])
        
        from models.geobox import GeoBox
        
        geobox = GeoBox.all()
        geobox.filter("lat =", oldGeoBoxId[0])
        geobox.filter("lon =", oldGeoBoxId[1])
        oldGeoBox = geobox.get()
        
        if oldGeoBox == None:
            oldGeoBox = GeoBox(
                lat = oldGeoBoxId[0],
                lon = oldGeoBoxId[1]
            )
            oldGeoBox.put()
        
        db.run_in_transaction(self.removeFromGeoBox, oldGeoBox.key(), latestAttraction.id)
        
        try:
            newId = db.run_in_transaction(self.createAttraction, latestAttraction.key(), attraction)
            
            geobox = GeoBox.all()
            geobox.filter("lat =", newGeoBoxId[0])
            geobox.filter("lon =", newGeoBoxId[1])
            newGeoBox = geobox.get()
            
            if newGeoBox == None:
                newGeoBox = GeoBox(
                    lat = newGeoBoxId[0],
                    lon = newGeoBoxId[1]
                )
                newGeoBox.put()
            
            db.run_in_transaction(self.addToGeoBox, newGeoBox.key(), newId)
            
            return newId
            
        except db.TransactionFailedError: # undo geobox update
            db.run_in_transaction(self.addToGeoBox, oldGeoBox.key(), latestAttraction.id)
    
    def calcGeoBoxId(self, lat, lon):
        return (round(float(lat), 1), round(float(lon), 1))
    
    def addToGeoBox(self, key, attractionId):
        geoBox = db.get(key)
        try:
            geoBox.attractions.append(attractionId)
            geoBox.put()
        except:
            pass
    
    def removeFromGeoBox(self, key, attractionId):
        geoBox = db.get(key)
        try:
            geoBox.attractions.remove(attractionId)
            geoBox.put()
        except:
            pass
    
    def createAttraction(self, key, attractionData):
        
        from google.appengine.api import users
        
        oldAttraction = db.get(key)
        
        newAttraction = Attraction(
            parent = oldAttraction,
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
            tags = attractionData['tags'],
            free = oldAttraction.free,
            rating = oldAttraction.rating,
            user = attractionData['user']
        )
        
        import md5
        newAttraction.id = md5.new(unicode(newAttraction)).hexdigest()
        oldAttraction.next = newAttraction.id
        
        oldAttraction.put()
        newAttraction.put()
        
        return newAttraction.id

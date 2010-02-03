from google.appengine.ext import db
import re

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
        
        if float(attraction['location']['lat']) < -90 or float(attraction['location']['lat']) > 90:
            errors['location'] = True
        
        if float(attraction['location']['lon']) < -180 or float(attraction['location']['lon']) > 180:
            errors['location'] = True
        
        if not len(attraction['href']) == 0 and not re.match(r"^https?://.+$", attraction['href']):
            errors['href'] = True
        
        if not len(attraction['picture']) == 0 and not re.match(r"^https?://.+$", attraction['picture']):
            errors['picture'] = True
        
        for tag in attraction['tags']:
            if not re.match(r"^[a-z0-9]+$", tag):
                errors['tags'] = True
        
        if errors or (self.request.get('location.x') and self.request.get('location.y')):
            
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
                
                oldGeoBoxId = self.calcGeoBoxId(latestAttraction.location.lat, latestAttraction.location.lon)
                newGeoBoxId = self.calcGeoBoxId(attraction['location']['lat'], attraction['location']['lon'])
                if True or oldGeoBoxId[0] != newGeoBoxId[0] or oldGeoBoxId[1] != newGeoBoxId[1]: # attraction has moved, update geoboxes
                    
                    #self.response.out.write(str(oldGeoBoxId[0]) + "," + str(oldGeoBoxId[1]) + "\n")
                    #self.response.out.write(str(newGeoBoxId[0]) + "," + str(newGeoBoxId[1]) + "\n")
                    
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
                        newId = db.run_in_transaction(self.saveAttraction, latestAttraction.key(), attraction)
                        
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
                        
                        self.redirect('/attractions/' + newId + '.html')
                        return
                        
                    except db.TransactionFailedError: # undo geobox update
                        pass
                    
                else:
                    
                    newId = db.run_in_transaction(self.saveAttraction, latestAttraction.key(), attraction)
                    
                    self.redirect('/attractions/' + newId + '.html')
                    return
                    
            except:
                pass
            
            template_values = {
                'attraction': attraction,
                'errors': {
                    'save': True
                }
            }
            self.output('edit', 'html', template_values)
    
    
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
    
    def saveAttraction(self, key, attractionData):
        
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
            user = None
        )
        
        import md5
        newAttraction.id = md5.new(unicode(newAttraction)).hexdigest()
        oldAttraction.next = newAttraction.id
        
        oldAttraction.put()
        newAttraction.put()
        
        return newAttraction.id

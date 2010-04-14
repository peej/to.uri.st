from google.appengine.ext import db
import re

from controllers.controller import Controller
from models.attraction import Attraction

class RecentPage(Controller):
    
    def get(self, type):
        
        coords = self.request.get("c")
        page = int(self.request.get("page", 1));
        
        template_values = {}
        
        if coords:
            coords = coords.split(',')
            
            lat = round(float(coords[0]), 1)
            lon = round(float(coords[1]), 1)
            
            lats = [lat - 0.1, lat, lat + 0.1]
            lons = [lon - 0.1, lon, lon + 0.1]
            
            attractions = []
            count = 0
            
            for latitude in lats:
                for longitude in lons:
                    
                    query = Attraction.all()
                    query.filter("next =", None)
                    query.filter("geobox =", '%s,%s' % (latitude, longitude))
                    query.order("-datetime")
                    
                    try:
                        #fetched = query.fetch(26, ((page - 1) * 26) + count)
                        #for attraction in fetched:
                        for attraction in query:
                            count = count + 1
                            if count > (page - 1) * 26:
                                attractions.append(attraction)
                            if count >= (page - 1) * 26 + 26:
                                break
                    except (IndexError, db.BadRequestError):
                        pass
                    
                    if count >= 26:
                        break
                if count >= 26:
                    break
                    
            attractions.sort()
            
            template_values['coords'] = '%.1f,%.1f' % (lat, lon)
            template_values['atomtag'] = 'recent:' + template_values['coords']
            
            if page > 1:
                template_values['previous'] = self.request.path + '?c=%.1f,%.1f&page=%d' % (lat, lon, page - 1)
            
            if count == 26:
                template_values['next'] = self.request.path + '?c=%.1f,%.1f&page=%d' % (lat, lon, page + 1)
            
        else:
            
            query = Attraction.all()
            query.filter("next =", None)
            query.order("-datetime")
            
            try:
                attractions = query.fetch(26, (page - 1) * 26)
            except (IndexError, db.BadRequestError):
                attractions = []
                
            if page > 1:
                template_values['previous'] = self.request.path + '?page=' + str(page - 1)
            
            if len(attractions) == 26:
                template_values['next'] = self.request.path + '?page=' + str(page + 1)
            
            template_values['atomtag'] = 'recent'
        
        updated = None
        numberOfAttractions = len(attractions)
        attractionCount = 64
        for attraction in attractions:
            attractionCount = attractionCount + 1
            if attractionCount < 91:
                attraction.label = chr(attractionCount)
            if updated == None or attraction.datetime > updated:
                updated = attraction.datetime
            if attraction.picture:
                attraction.thumbnail = self.convertFlickrUrl(attraction.picture, "s")
        
        template_values['attractions'] = attractions
        template_values['updated'] = updated
        
        template_values['url'] = self.request.url
        template_values['atom'] = re.sub(r'\..+$', '.atom', self.request.path)
        template_values['sitemap'] = re.sub(r'\..+$', '.xml', self.request.path)
        template_values['kml'] = re.sub(r'\.[^.]+$', '.kml', self.request.url)
        
        if type == 'xml':
            template_values['cities'] = self.cities
        
        self.output('recent', type, template_values)
        

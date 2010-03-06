from google.appengine.ext import db

from controllers.controller import Controller
from models.attraction import Attraction

class RecentPage(Controller):
    
    def get(self, type):
        
        coords = self.request.get("c")
        
        template_values = {}
        
        if coords:
            coords = coords.split(',')
            
            lat = round(float(coords[0]), 1)
            lon = round(float(coords[1]), 1)
            
            lats = [lat - 0.1, lat, lat + 0.1]
            lons = [lon - 0.1, lon, lon + 0.1]
            
            attractions = []
            
            from models.geobox import GeoBox
            
            for latitude in lats:
                for longitude in lons:
                    
                    geobox = GeoBox.all()
                    geobox.filter("lat =", latitude)
                    geobox.filter("lon =", longitude)
                    
                    geoboxes = geobox.get()
                    
                    if geoboxes:
                        for attractionId in geoboxes.attractions:
                            attractionQuery = Attraction.all()
                            attractionQuery.filter("id =", attractionId)
                            attractionQuery.filter("next =", None)
                            attraction = attractionQuery.get()
                            if attraction:
                                attractions.append(attraction)
            
            attractions.sort()
            
            template_values['coords'] = '%.1f,%.1f' % (lat, lon)
            template_values['atomtag'] = 'recent:' + template_values['coords']
            
        else:
            page = int(self.request.get("page", 1));
            
            recent = Attraction.all()
            recent.filter("next =", None)
            recent.order("-datetime")
            
            try:
                attractions = recent.fetch(26, (page - 1) * 26)
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
        
        template_values['attractions'] = attractions
        template_values['updated'] = updated
        
        template_values['url'] = self.request.url
        template_values['atom'] = self.request.url.replace('.html', '.atom')
        template_values['sitemap'] = self.request.url.replace('.html', '.xml')
        
        if type == 'xml':
            template_values['cities'] = self.cities
        
        self.output('recent', type, template_values)
        

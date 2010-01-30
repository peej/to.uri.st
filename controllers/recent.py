from google.appengine.ext import db

from controllers.controller import Controller
from models.attraction import Attraction

class RecentPage(Controller):
    
    def get(self):
        
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
            
        else:
            page = int(self.request.get("page", 1));
            
            recent = Attraction.all()
            recent.filter("next =", None)
            recent.order("-datetime")
            
            attractions = recent.fetch(26, (page - 1) * 26)
            
            if page > 1:
                template_values['previous'] = self.request.path + '?page=' + str(page - 1)
            template_values['next'] = self.request.path + '?page=' + str(page + 1)
        
        numberOfAttractions = len(attractions)
        attractionCount = 64
        for attraction in attractions:
            attractionCount = attractionCount + 1
            if attractionCount < 91:
                attraction.label = chr(attractionCount)
        
        template_values['attractions'] = attractions
        
        self.output('recent', 'html', template_values)
        

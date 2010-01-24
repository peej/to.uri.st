import urllib, json
from google.appengine.ext import db

from controllers.controller import Controller
from models.attraction import Attraction
from models.geobox import GeoBox

class SearchPage(Controller):
    
    def getAttractions(self, lat, lon):
        
        lat = round(lat, 1)
        lon = round(lon, 1)
        
        lats = [lat, lat + 0.1]
        lons = [lon, lon + 0.1]
        
        attractions = []
        
        for latitude in lats:
            for longitude in lons:
                
                geobox = GeoBox.all()
                geobox.filter("lat =", latitude)
                geobox.filter("lon =", longitude)
                
                geoboxes = geobox.get()
                
                if geoboxes:
                    for attractionId in geoboxes.attractions:
                        attraction = Attraction.all()
                        attraction.filter("id =", attractionId)
                        attractions.append(attraction.get())
        
        numberOfAttractions = len(attractions)
        attractionCount = 64
        for attraction in attractions:
            attractionCount = attractionCount + 1
            if attractionCount < 91:
                attraction.label = chr(attractionCount)
            
        return attractions
    
    def get(self):
        
        search = self.request.get("q")
        coords = self.request.get("c")
        
        template_values = {}
        
        if coords:
            
            url = "http://maps.google.com/maps/geo?q=%s&sensor=false" % urllib.quote(coords)
            
            template_values['coords'] = coords
            
            jsonString = urllib.urlopen(url).read()
            if jsonString:
                data = json.loads(jsonString)
                try:
                    lat = data['Placemark'][0]['Point']['coordinates'][1]
                    lon = data['Placemark'][0]['Point']['coordinates'][0]
                    template_values['attractions'] = self.getAttractions(lat, lon)
                    try:
                        template_values['search'] = "%s, %s" % (
                            data['Placemark'][0]['AddressDetails']['Country']['AdministrativeArea']['SubAdministrativeArea']['SubAdministrativeAreaName'],
                            data['Placemark'][0]['AddressDetails']['Country']['CountryName']
                        )
                    finally:
                        pass
                finally:
                    pass
            else:
                parts = coords.split(",")
                lat = parts[0]
                lon = parts[1]
                template_values['attractions'] = self.getAttractions(lat, lon)
            
        else:
            
            url = "http://maps.google.com/maps/geo?q=%s&sensor=false" % urllib.quote(search)
            
            template_values['search'] = search,
            
            jsonString = urllib.urlopen(url).read()
            if jsonString:
                data = json.loads(jsonString)
                try:
                    lat = data['Placemark'][0]['Point']['coordinates'][1]
                    lon = data['Placemark'][0]['Point']['coordinates'][0]
                    template_values['coords'] = "%.1f,%.1f" % (lat, lon)
                    if len(data['Placemark']) > 1:
                        template_values['results'] = data['Placemark']
                    else:
                        template_values['attractions'] = self.getAttractions(lat, lon)
                        try:
                            template_values['search'] = "%s, %s" % (
                                data['Placemark'][0]['AddressDetails']['Country']['AdministrativeArea']['SubAdministrativeArea']['SubAdministrativeAreaName'],
                                data['Placemark'][0]['AddressDetails']['Country']['CountryName']
                            )
                        finally:
                            pass
                finally:
                    pass
            
        template_values['q'] = search
        self.output('search.html', template_values)
        

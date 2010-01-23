import urllib, json
from google.appengine.ext import db

from controllers.controller import Controller
from models.attraction import Attraction
from models.geobox import GeoBox

class SearchPage(Controller):
    
    def getAttractions(self, lat, lon):
        
        lat = round(lat, 1)
        lon = round(lon, 1)
        
        lats = [lat - 0.1, lat, lat + 0.1]
        lons = [lon - 0.1, lon, lon + 0.1]
        
        attractions = []
        
        markerCount = 0
        markerColour = 0;
        markerColours = ['red', 'green', 'yellow', 'blue']
        
        for latitude in lats:
            for longitude in lons:
                
                geobox = GeoBox.all()
                geobox.filter("lat =", latitude)
                geobox.filter("lon =", longitude)
                
                geoboxes = geobox.get()
                
                if geoboxes:
                    for attractionId in geoboxes.attractions:
                        markerCount = markerCount + 1
                        if markerCount > 26:
                            markerCount = 1
                            markerColour = markerColour + 1
                        attraction = Attraction.all()
                        attraction.filter("id =", attractionId)
                        a = attraction.get()
                        a.marker = chr(markerCount + 64)
                        a.colour = markerColours[markerColour]
                        attractions.append(a)
        
        return attractions
    
    def get(self):
        
        search = self.request.get("q")
        coords = self.request.get("c")
        
        if coords:
            
            url = "http://maps.google.com/maps/geo?q=%s&sensor=false" % coords
            
            jsonString = urllib.urlopen(url).read()
            if jsonString:
                data = json.loads(jsonString)
                try:
                    lat = data['Placemark'][0]['Point']['coordinates'][1]
                    lon = data['Placemark'][0]['Point']['coordinates'][0]
                    try:
                        template_values = {
                            'search': "%s, %s" % (
                                data['Placemark'][0]['AddressDetails']['Country']['AdministrativeArea']['SubAdministrativeArea']['SubAdministrativeAreaName'],
                                data['Placemark'][0]['AddressDetails']['Country']['CountryName']
                            ),
                            'coords': coords,
                            'attractions': self.getAttractions(lat, lon)
                        }
                    except KeyError:
                        template_values = {
                            'coords': coords,
                            'attractions': self.getAttractions(lat, lon)
                        }
                except KeyError:
                    template_values = {
                        'coords': coords,
                        'error': True
                    }
            else:
                parts = coords.split(",")
                lat = parts[0]
                lon = parts[1]
                template_values = {
                    'coords': coords,
                    'attractions': self.getAttractions(lat, lon)
                }
            
            self.output('search.html', template_values)
            
        else:
            
            url = "http://maps.google.com/maps/geo?q=%s&sensor=false" % urllib.quote(search)
            
            jsonString = urllib.urlopen(url).read()
            if jsonString:
                data = json.loads(jsonString)
                try:
                    lat = data['Placemark'][0]['Point']['coordinates'][1]
                    lon = data['Placemark'][0]['Point']['coordinates'][0]
                    if len(data['Placemark']) > 1:
                        template_values = {
                            'search': search,
                            'coords': lat + ',' + lon,
                            'results': data['Placemark']
                        }
                    else:
                        try:
                            template_values = {
                                'search': "%s, %s" % (
                                    data['Placemark'][0]['AddressDetails']['Country']['AdministrativeArea']['SubAdministrativeArea']['SubAdministrativeAreaName'],
                                    data['Placemark'][0]['AddressDetails']['Country']['CountryName']
                                ),
                                'coords': "%.1f,%.1f" % (lat, lon),
                                'attractions': self.getAttractions(lat, lon)
                            }
                        except KeyError:
                            template_values = {
                                'search': search,
                                'coords': lat + ',' + lon,
                                'attractions': self.getAttractions(lat, lon)
                            }
                except KeyError:
                    template_values = {
                        'search': search,
                        'error': True
                    }
            else:
                template_values = {
                    'search': search,
                    'error': True
                }
            
            template_values['q'] = search
            self.output('search.html', template_values)
        

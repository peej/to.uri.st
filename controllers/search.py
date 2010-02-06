import urllib, datetime
from django.utils import simplejson
from google.appengine.ext import db

from controllers.controller import Controller
from models.attraction import Attraction
from models.geobox import GeoBox

class SearchPage(Controller):
    
    def getAttractions(self, lat, lon, type):
        
        lat = round(lat, 1)
        lon = round(lon, 1)
        
        if type == 'js':
            lats = [lat]
            lons = [lon]
        else:
            lats = [lat - 0.1, lat, lat + 0.1]
            lons = [lon - 0.1, lon, lon + 0.1]
        
        attractions = []
        updated = None
        
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
                            if updated == None or attraction.datetime > updated:
                                updated = attraction.datetime
        
        numberOfAttractions = len(attractions)
        attractionCount = 64
        for attraction in attractions:
            attractionCount = attractionCount + 1
            if attractionCount < 91:
                attraction.label = chr(attractionCount)
            
        return (attractions, updated)
    
    def get(self, type):
        
        search = self.request.get("q")
        coords = self.request.get("c")
        tag = self.request.get("t")
        
        template_values = {}
        
        if coords:
            
            coords = coords.split(',')
            
            url = "http://maps.google.com/maps/geo?q=%.2f,%.2f&sensor=false" % (float(coords[0]), float(coords[1]))
            
            template_values['coords'] = "%.2f,%.2f" % (float(coords[0]), float(coords[1]))
            
            jsonString = urllib.urlopen(url).read()
            if jsonString:
                data = simplejson.loads(jsonString)
                try:
                    lat = data['Placemark'][0]['Point']['coordinates'][1]
                    lon = data['Placemark'][0]['Point']['coordinates'][0]
                    (template_values['attractions'], template_values['updated']) = self.getAttractions(lat, lon, type)
                    if (
                        'Country' in data['Placemark'][0]['AddressDetails'] and 
                        'AdministrativeArea' in data['Placemark'][0]['AddressDetails']['Country'] and
                        'SubAdministrativeArea' in data['Placemark'][0]['AddressDetails']['Country']['AdministrativeArea'] and
                        'SubAdministrativeAreaName' in data['Placemark'][0]['AddressDetails']['Country']['AdministrativeArea']['SubAdministrativeArea'] and
                        'CountryName' in data['Placemark'][0]['AddressDetails']['Country']
                    ):
                        template_values['search'] = "%s, %s" % (
                            data['Placemark'][0]['AddressDetails']['Country']['AdministrativeArea']['SubAdministrativeArea']['SubAdministrativeAreaName'],
                            data['Placemark'][0]['AddressDetails']['Country']['CountryName']
                        )
                finally:
                    pass
            else:
                parts = coords.split(",")
                lat = parts[0]
                lon = parts[1]
                (template_values['attractions'], template_values['updated']) = self.getAttractions(lat, lon, type)
            
        elif search:
            
            url = "http://maps.google.com/maps/geo?q=%s&sensor=false" % urllib.quote(search)
            
            template_values['search'] = search,
            
            jsonString = urllib.urlopen(url).read()
            if jsonString:
                data = simplejson.loads(jsonString)
                try:
                    lat = data['Placemark'][0]['Point']['coordinates'][1]
                    lon = data['Placemark'][0]['Point']['coordinates'][0]
                    template_values['coords'] = "%.1f,%.1f" % (lat, lon)
                    if len(data['Placemark']) > 1:
                        template_values['results'] = data['Placemark']
                    else:
                        (template_values['attractions'], template_values['updated']) = self.getAttractions(lat, lon, type)
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
            
        elif tag:
            page = int(self.request.get("page", 1));
                        
            attractionQuery = Attraction.all()
            attractionQuery.filter("tags =", tag)
            attractionQuery.filter("next =", None)
            template_values['attractions'] = attractionQuery.fetch(26, (page - 1) * 26)
            
            if page > 1:
                template_values['previous'] = self.request.path + '?t=' + tag + '&page=' + str(page - 1)
            template_values['next'] = self.request.path + '?t=' + tag + '&page=' + str(page + 1)
            
            template_values['updated'] = None
            for attraction in template_values['attractions']:
                if template_values['updated'] == None or attraction.datetime > template_values['updated']:
                    template_values['updated'] = attraction.datetime
            
            template_values['tag'] = tag
        
        template_values['url'] = self.request.url
        
        template_values['atom'] = self.request.url.replace('.html', '.atom')
        template_values['json'] = self.request.url.replace('.html', '.js')
        
        self.output('search', type, template_values)


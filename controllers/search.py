import urllib, json
from google.appengine.ext import db

from controllers.controller import Controller
from models.attraction import Attraction

class SearchPage(Controller):
    def get(self):
        
        search = self.request.get("q")
        coords = self.request.get("c")
        
        if coords:
            
            url = "http://maps.google.com/maps/geo?q=%s&sensor=false" % coords
            
            jsonString = urllib.urlopen(url).read()
            if jsonString:
                data = json.loads(jsonString)
                try:
                    template_values = {
                        'search': "%s, %s" % (
                            data['Placemark'][0]['AddressDetails']['Country']['AdministrativeArea']['AdministrativeAreaName'],
                            data['Placemark'][0]['AddressDetails']['Country']['CountryName']
                        )
                    }
                except KeyError:
                    template_values = {
                        'search': coords,
                        'error': True
                    }
            else:
                template_values = {
                    'search': coords,
                    'error': True
                }
            
            self.output('search.html', template_values)
            
        else:
            
            url = "http://maps.google.com/maps/geo?q=%s&sensor=false" % urllib.quote(search)
            
            jsonString = urllib.urlopen(url).read()
            if jsonString:
                data = json.loads(jsonString)
                try:
                    if len(data['Placemark']) > 1:
                        template_values = {
                            'search': search,
                            'results': data['Placemark']
                        }
                    else:
                        self.response.set_status(302)
                        self.response.headers.add_header('Location', "/search.html?c=%.4f,%.4f" % (data['Placemark'][0]['Point']['coordinates'][1], data['Placemark'][0]['Point']['coordinates'][0]))
                        return
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
                
            self.output('search.html', template_values)
        

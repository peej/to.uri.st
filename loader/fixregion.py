from google.appengine.api.labs import taskqueue
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import datetime
from django.utils import simplejson
import urllib

from models.attraction import Attraction

class FixRegionWorker(webapp.RequestHandler):
    def get(self):
        n = self.request.get('n') or 1
        f = self.request.get('f') or 1
        
        taskqueue.add(
            url = '/fixregion',
            params = {
                'n': n,
                'f': f
            }
        )
        
        self.response.out.write("running")
    
    def post(self):
        n = int(self.request.get('n'))
        l = 50
        f = self.request.get('f')
        
        import csv
        
        csvReader = csv.reader(open('attractions' + f + '.csv'))
        
        count = 1
        for row in csvReader:
            
            if count >= n and count < n + l:
                
                q = Attraction.all()
                q.filter("id =", row[0])
                attraction = q.get()
                
                if attraction:
                    
                    location = row[1].split(',')
                    
                    url = "http://maps.google.com/maps/geo?q=%.2f,%.2f&sensor=false" % (float(location[0]), float(location[1]))
                    jsonString = urllib.urlopen(url).read()
                    if jsonString:
                        data = simplejson.loads(jsonString)
                        if 'Placemark' in data:
                            for placemark in data['Placemark']:
                                try:
                                    attraction.region = u"%s, %s" % (
                                        placemark['AddressDetails']['Country']['AdministrativeArea']['SubAdministrativeArea']['SubAdministrativeAreaName'],
                                        placemark['AddressDetails']['Country']['CountryName']
                                    )
                                    break;
                                except KeyError:
                                    try:
                                        attraction.region = u"%s, %s" % (
                                            placemark['AddressDetails']['Country']['AdministrativeArea']['Locality']['LocalityName'],
                                            placemark['AddressDetails']['Country']['CountryName']
                                        )
                                        break;
                                    except KeyError:
                                        attraction.region = 'Unknown location'
                        else:
                            attraction.region = 'Unknown location'
                    else:
                        attraction.region = 'Unknown location'
                    
                    attraction.put()
                
            elif count >= n:
                
                taskqueue.add(
                    url = '/fixregion',
                    params = {
                        'n': n + l,
                        'f': f
                    }
                )
                break
            
            count = count  + 1
        

def main():
    run_wsgi_app(webapp.WSGIApplication([
        ('/fixregion', FixRegionWorker),
    ]))

if __name__ == '__main__':
    main()

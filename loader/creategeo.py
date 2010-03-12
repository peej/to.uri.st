from google.appengine.api.labs import taskqueue
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import datetime

from models.attraction import Attraction

class CreateGeoWorker(webapp.RequestHandler):
    def get(self):
        n = self.request.get('n') or 1
        f = self.request.get('f') or 1
        
        taskqueue.add(
            url = '/creategeo',
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
                    
                    attraction.geobox = str(round(float(attraction.location.lat), 1)) + ',' + str(round(float(attraction.location.lon), 1))
                    attraction.put()
                
            elif count >= n:
                
                taskqueue.add(
                    url = '/creategeo',
                    params = {
                        'n': n + l,
                        'f': f
                    }
                )
                break
            
            count = count  + 1
        

def main():
    run_wsgi_app(webapp.WSGIApplication([
        ('/creategeo', CreateGeoWorker),
    ]))

if __name__ == '__main__':
    main()

from google.appengine.api.labs import taskqueue
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from models.geobox import GeoBox

class DeDupeWorker(webapp.RequestHandler):
    def get(self):
        n = self.request.get('n') or 1
        f = self.request.get('f') or 1
        
        taskqueue.add(
            url = '/dedupe',
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
                
                parts = row[1].split(',')
                lat = round(float(parts[0]), 1)
                lon = round(float(parts[1]), 1)
                
                query = GeoBox.all()
                query.filter("lat =", lat)
                query.filter("lon =", lon)
                geoBox = query.get()
                
                if geoBox:
                    keys = {}
                    for e in geoBox.attractions:
                        keys[e] = 1
                    geoBox.attractions = keys.keys()
                    geoBox.put()
                
            elif count >= n:
                
                taskqueue.add(
                    url = '/dedupe',
                    params = {
                        'n': n + l,
                        'f': f
                    }
                )
                break
            
            count = count  + 1
        
        if f < 4:
            taskqueue.add(
                url = '/dedupe',
                params = {
                    'n': n + l,
                    'f': f + 1
                }
            )

def main():
    run_wsgi_app(webapp.WSGIApplication([
        ('/dedupe', DeDupeWorker),
    ]))

if __name__ == '__main__':
    main()

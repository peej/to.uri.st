from google.appengine.api.labs import taskqueue
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import datetime

from models.attraction import Attraction

class FixDateWorker(webapp.RequestHandler):
    def get(self):
        n = self.request.get('n') or 1
        
        taskqueue.add(
            url = '/fixdate',
            params = {
                'n': n
            }
        )
        
        self.response.out.write("running")
    
    def post(self):
        n = int(self.request.get('n'))
        l = 50
        
        import csv
        
        csvReader = csv.reader(open('attractions4.csv'))
        
        count = 1
        for row in csvReader:
            
            if count >= n and count < n + l:
                
                attractions = Attraction.all()
                attractions.filter("id =", row[0])
                attraction = attractions.get()
                
                if attraction:
                    attraction.datetime = datetime.datetime(
                        year = int(row[8][0:4]),
                        month = int(row[8][5:7]),
                        day = int(row[8][8:10]),
                        hour = int(row[8][11:13]),
                        minute = int(row[8][14:16]),
                        second = int(row[8][17:19])
                    )
                    attraction.put()
                
            elif count >= n:
                
                taskqueue.add(
                    url = '/fixdate',
                    params = {
                        'n': n + l,
                    }
                )
                break
            
            count = count  + 1

def main():
    run_wsgi_app(webapp.WSGIApplication([
        ('/fixdate', FixDateWorker),
    ]))

if __name__ == '__main__':
    main()

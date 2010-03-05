from google.appengine.api.labs import taskqueue
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from models.attraction import Attraction

class DeDupeWorker(webapp.RequestHandler):
    def get(self):
        n = self.request.get('n') or 1
        
        taskqueue.add(
            url = '/dedupe',
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
                attractionObjects = attractions.fetch(50)
                
                deleteIt = False
                for attraction in attractionObjects:
                    if deleteIt:
                        attraction.delete()
                    else:
                        deleteIt = True
                
            elif count >= n:
                
                taskqueue.add(
                    url = '/dedupe',
                    params = {
                        'n': n + l,
                    }
                )
                break
            
            count = count  + 1

def main():
    run_wsgi_app(webapp.WSGIApplication([
        ('/dedupe', DeDupeWorker),
    ]))

if __name__ == '__main__':
    main()

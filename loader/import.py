from google.appengine.api.labs import taskqueue
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import datetime

from models.attraction import Attraction

class ImportWorker(webapp.RequestHandler):
    def get(self):
        n = self.request.get('n') or 1
        
        taskqueue.add(
            url = '/import',
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
                if not attraction:
                    
                    location = row[1].split(',')
                    
                    if row[7] == 'y':
                        freeVal = True
                    else:
                        freeVal = False
                    
                    name = row[2].decode('utf-8').replace("\n", ' ')
                    if name == '':
                        name = 'No name'
                    
                    try:
                        newAttraction = Attraction(
                            id = row[0],
                            root = row[0],
                            name = name,
                            region = row[6].decode('utf-8').replace("\n", ' '),
                            description = row[3].decode('utf-8'),
                            location = db.GeoPt(
                                lat = location[0],
                                lon = location[1]
                            ),
                            href = row[4].decode('utf-8'),
                            picture = row[5].decode('utf-8'),
                            free = freeVal,
                            datetime = datetime.datetime(
                                year = int(row[8][0:4]),
                                month = int(row[8][5:7]),
                                day = int(row[8][8:10]),
                                hour = int(row[8][11:13]),
                                minute = int(row[8][14:16]),
                                second = int(row[8][17:19])
                            )
                        )
                        
                        newGeoBoxId = (round(float(location[0]), 1), round(float(location[1]), 1))
                        
                        from models.geobox import GeoBox
                        
                        geobox = GeoBox.all()
                        geobox.filter("lat =", newGeoBoxId[0])
                        geobox.filter("lon =", newGeoBoxId[1])
                        newGeoBox = geobox.get()
                        
                        if newGeoBox == None:
                            newGeoBox = GeoBox(
                                lat = newGeoBoxId[0],
                                lon = newGeoBoxId[1]
                            )
                            newGeoBox.put()
                            
                        newGeoBox.attractions.append(row[0])
                        
                        newAttraction.put()
                        newGeoBox.put()
                        
                    except db.BadValueError:
                        pass
                
            elif count >= n:
                
                taskqueue.add(
                    url = '/import',
                    params = {
                        'n': n + l,
                    }
                )
                break
            
            count = count  + 1

def main():
    run_wsgi_app(webapp.WSGIApplication([
        ('/import', ImportWorker),
    ]))

if __name__ == '__main__':
    main()

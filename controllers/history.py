from google.appengine.ext import db
import re, difflib

from controllers.controller import Controller
from models.attraction import Attraction

class HistoryPage(Controller):
    def get(self, attractionId):
        
        attractions = []
        
        query = Attraction.all()
        query.filter("id =", attractionId)
        attraction = query.get()
        
        while attraction.next != None:
            query = Attraction.all()
            query.filter("id =", attraction.next)
            attraction = query.get()
            attractions.insert(0, attraction)
        
        while attractionId:
            query = Attraction.all()
            query.filter("id =", attractionId)
            attraction = query.get()
            attractions.append(attraction)
            attractionId = attraction.previous if attraction.previous else False
        
        for index in range(0, len(attractions) - 1):
            oldAttr = attractions[index + 1]
            newAttr = attractions[index]
            attractions[index].diff = []
            
            diffString = "Name: %s\nRegion: %s\nLocation: %.4f,%.4f\nMore info: %s\n\n%s"
            
            old = diffString % (
                oldAttr.name,
                oldAttr.region,
                oldAttr.location.lat,
                oldAttr.location.lon,
                oldAttr.href,
                oldAttr.description
            )
            new = diffString % (
                newAttr.name,
                newAttr.region,
                newAttr.location.lat,
                newAttr.location.lon,
                newAttr.href,
                newAttr.description
            )
            
            diff = difflib.unified_diff(old.splitlines(1), new.splitlines(1), n = 3)
            for line in diff:
                if line[0:3] != '---' and line[0:3] != '+++' and line[0:2] != '@@':
                    #line = re.sub(r'Picture: (.+)', r'Picture: <img src="\1" alt="">', line)
                    if line[0:1] == '+':
                        attractions[index].diff.append(('add', line.strip(" \n+")))
                    elif line[0:1] == '-':
                        attractions[index].diff.append(('take', line.strip(" \n-")))
                    else:
                        attractions[index].diff.append(('', line.strip()))
            
            oldPic = self.convertFlickrUrl(oldAttr.picture, 's')
            newPic = self.convertFlickrUrl(newAttr.picture, 's')
            if oldPic != newPic:
                attractions[index].diff.append(('pic', oldPic, newPic))
        
        template_values = {
            'name': attraction.name,
            'attractions': attractions
        }
        
        self.output('history.html', template_values)
        

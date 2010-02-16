from google.appengine.ext import db

import re

from controllers.controller import Controller
from models.attraction import Attraction

class AttractionPage(Controller):
    def get(self, attractionId, type):
        
        attractions = Attraction.all()
        attractions.filter("id =", attractionId)
        attraction = attractions.get()
        
        if attraction:
            attraction.picture = self.convertFlickrUrl(attraction.picture, 'm')
            
            if attraction.user:
                attraction.userid = self.getUserId(attraction.user)
                attraction.nickname = attraction.user.nickname()
            
            result = re.split('\n\n--', attraction.description)
            if result:
                attraction.description = result[0]
                comments = result[1:]
                attraction.comments = []
                for comment in comments:
                    exploded = re.split('\n\n', comment)
                    attraction.comments.append({
                        "user": exploded[0],
                        "userid": self.getUserId(exploded[0]),
                        "comment": "\n\n".join(exploded[1:])
                    })
            
            template_values = {
                'attraction': attraction,
                'gpx': self.request.url.replace('.html', '.gpx')
            }
            
            self.output('attraction', type, template_values)
        else:
            self.output('404', 'html')

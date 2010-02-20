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
            
            result = re.split('\r\n\r\n--', attraction.description)
            if result:
                attraction.description = result[0]
                comments = result[1:]
                attraction.comments = []
                for comment in comments:
                    exploded = re.split('\r\n\r\n', comment)
                    attraction.comments.append({
                        "user": exploded[0],
                        "userid": self.getUserId(exploded[0]),
                        "comment": "\r\n\r\n".join(exploded[1:])
                    })
            
            from google.appengine.api import users
            user = users.get_current_user()
            userObject = self.getUserObject(user)
            
            if attraction.root in userObject.favourites:
                favourite = True
            else:
                favourite = False
            
            if attraction.root in userObject.recommended:
                recommended = True
            else:
                recommended = False
            
            if attraction.root in userObject.itinerary:
                itinerary = True
            else:
                itinerary = False
            
            template_values = {
                'attraction': attraction,
                'gpx': self.request.url.replace('.html', '.gpx'),
                'favourite': favourite,
                'recommended': recommended,
                'itinerary': itinerary
            }
            
            self.output('attraction', type, template_values)
        else:
            self.output('404', 'html')

from google.appengine.ext import db

from controllers.controller import Controller
from models.attraction import Attraction
from models.user import User

class HomePage(Controller):
    def get(self, type = 'html'):
        
        recent = Attraction.all()
        recent.filter("next =", None)
        recent.order("-datetime")
        
        popular = Attraction.all()
        popular.filter("next =", None)
        popular.order("-rating")
        
        users = User.all()
        users.order("activity")
        
        template_values = {
            'recent': recent.fetch(10),
            'popular': popular.fetch(5),
            'users': users.fetch(5),
            'service': '/home.atom',
            'opensearch': '/home.search'
        }
        
        for attraction in template_values['recent']:
            attraction.thumbnail = self.convertFlickrUrl(attraction.picture, 's')
        
        for attraction in template_values['popular']:
            attraction.thumbnail = self.convertFlickrUrl(attraction.picture, 's')
        
        self.output('home', type, template_values)
        

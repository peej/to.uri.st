from google.appengine.ext import db
import re

from controllers.controller import Controller
from models.attraction import Attraction
from models.user import User

class UserPage(Controller):
    
    def get(self, userid, type):
        
        query = User.all()
        query.filter("id =", userid)
        userObject = query.get()
        
        from google.appengine.api import users
        user = users.get_current_user()
        
        if self.getUserId(user) == userid:
            owner = True
        else:
            owner = False
        
        if not userObject and owner:
            userObject = self.getUserObject(user)
        
        if userObject:
            
            template_values = {
                'user': userObject,
                'owner': owner,
                'badges': self.badges
            }
            
            edited = Attraction.all()
            edited.filter("userid =", userid)
            edited.filter("next =", None)
            edited.order("-datetime")
            
            if edited.count() > 0:
                template_values['edited'] = edited.fetch(10)
                for attraction in template_values['edited']:
                    attraction.thumbnail = self.convertFlickrUrl(attraction.picture, 's')
            
            template_values['updated'] = None
            for attraction in edited:
                if template_values['updated'] == None or attraction.datetime > template_values['updated']:
                    template_values['updated'] = attraction.datetime
            
            recommended = Attraction.all()
            recommended.filter("root IN", userObject.recommended)
            recommended.filter("next =", None)
            recommended.order("-datetime")
            
            if recommended.count() > 0:
                template_values['recommended'] = recommended.fetch(10)
                for attraction in template_values['recommended']:
                    attraction.thumbnail = self.convertFlickrUrl(attraction.picture, 's')
            
            itinerary = Attraction.all()
            itinerary.filter("root IN", userObject.itinerary)
            itinerary.filter("next =", None)
            itinerary.order("-datetime")
            
            if itinerary.count() > 0:
                template_values['itinerary'] = itinerary.fetch(10)
                for attraction in template_values['itinerary']:
                    attraction.thumbnail = self.convertFlickrUrl(attraction.picture, 's')
            
            template_values['url'] = self.request.path
            template_values['atomtag'] = 'user:' + userid
            
            template_values['atom'] = re.sub(r'\..+$', '.atom', self.request.path)
            template_values['html'] = re.sub(r'\..+$', '.html', self.request.path)
            template_values['kml'] = re.sub(r'\.[^.]+$', '.kml', self.request.url)
            
            self.output('user', type, template_values)
            
        else:
            self.output('404', 'html')

from google.appengine.ext import db

from controllers.controller import Controller
from models.attraction import Attraction

class UserPage(Controller):
    
    def get(self, userid):
        
        userObject = self.getUserObject(userid)
        
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
            
            recommended = Attraction.all()
            recommended.filter("root IN", userObject.recommended)
            recommended.filter("next =", None)
            recommended.order("name")
            
            if recommended.count() > 0:
                template_values['recommended'] = recommended
            
            itinerary = Attraction.all()
            itinerary.filter("root IN", userObject.itinerary)
            itinerary.filter("next =", None)
            itinerary.order("name")
            
            if itinerary.count() > 0:
                template_values['itinerary'] = itinerary
                
            self.output('user', 'html', template_values)
        else:
            self.output('404', 'html')

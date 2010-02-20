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
            
            attractions = Attraction.all()
            attractions.filter("userid =", userid)
            attractions.filter("next =", None)
            attractions.order("-datetime")
            
            favourites = Attraction.all()
            favourites.filter("root IN", userObject.favourites)
            favourites.filter("next =", None)
            favourites.order("name")
            
            template_values = {
                'user': userObject,
                'owner': owner,
                'attractions': attractions.fetch(10),
                'favourites': favourites
            }
            
            self.output('user', 'html', template_values)
        else:
            self.output('404', 'html')

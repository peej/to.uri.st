from google.appengine.ext import db

from controllers.controller import Controller
from models.attraction import Attraction
from models.user import User

class Recommend(Controller):
    def get(self, attractionId):
        self.output('sure', 'html', {
            'yes': self.request.path,
            'no': '/attractions/' + attractionId + '.html'
        })
        
    def post(self, attractionId):
        
        from google.appengine.api import users
        user = users.get_current_user()
        
        if user:
            
            attractions = Attraction.all()
            attractions.filter("id =", attractionId)
            attraction = attractions.get()
            
            if attraction:
                
                userObject = self.getUserObject(user)
                
                if attraction.root in userObject.recommended:
                    userObject.recommended.remove(attraction.root)
                    if attraction.rating > 0:
                        attraction.rating = attraction.rating - 1
                else:
                    userObject.recommended.append(attraction.root)
                    if type(attraction.rating) == long:
                        attraction.rating = attraction.rating + 1
                    else:
                        attraction.rating = 1
                
                attraction.put()
                userObject.put()
                
                if attraction.userid != userObject.id:
                    query = User.all()
                    query.filter("id =", attraction.userid)
                    user = query.get()
                    
                    # update stats
                    self.addStat(user, 3) # recommended
                    
                    newBadges = self.updateBadges(user)
                    user.put()
                    
        self.redirect('/attractions/' + attractionId + '.html')
        return
        

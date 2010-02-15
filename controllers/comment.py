from google.appengine.ext import db

from controllers.edit import EditPage
from models.attraction import Attraction

class CommentAdd(EditPage):
    
    def post(self, attractionId):
        
        if self.request.get('comment'):
            
            next = attractionId
            while next: # walk to newest version of this attraction
                query = Attraction.all()
                query.filter("id =", next)
                latestAttraction = query.get()
                next = latestAttraction.next
            
            from google.appengine.api import users
            user = users.get_current_user()
            if user:
                username = user.nickname();
            else:
                username = self.request.remote_addr
            
            data = {}
            data['name'] = latestAttraction.name
            data['region'] = latestAttraction.region
            data['description'] = latestAttraction.description + "\n\n--" + username + "\n\n" + self.request.get('comment')
            data['location'] = {}
            data['location']['lat'] = latestAttraction.location.lat
            data['location']['lon'] = latestAttraction.location.lon
            data['href'] = latestAttraction.href
            data['picture'] = latestAttraction.picture
            data['tags'] = latestAttraction.tags
            data['free'] = latestAttraction.free
            data['rating'] = latestAttraction.rating
            data['user'] = user
            
            newId = self.saveAttraction(latestAttraction, data)
            
            self.getUserObject(user) # create user object if it doesn't exist
            
            self.redirect('/attractions/' + newId + '.html')
            return


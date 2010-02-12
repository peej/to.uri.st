from google.appengine.ext import db

from controllers.controller import Controller

class UserPage(Controller):
    
    def get(self, userid):
        
        from google.appengine.api import users
        user = users.get_current_user()
        print user.nickname()
        print user.user_id()
        print user.email()
        
        template_values = {
            'nickname': userid
        }
        
        #self.output('user', 'html', template_values)
        

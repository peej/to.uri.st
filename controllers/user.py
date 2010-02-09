from google.appengine.ext import db

from controllers.controller import Controller

class UserPage(Controller):
    
    def get(self, userid):
        
        template_values = {
            'nickname': userid
        }
        
        self.output('user', 'html', template_values)
        

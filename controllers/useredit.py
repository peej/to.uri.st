from google.appengine.ext import db
import re

from controllers.controller import Controller
from models.user import User

class UserEdit(Controller):
    
    def get(self, userId = None):
        
        template_values = {}
        
        self.output('useredit', 'html', template_values)
    
    

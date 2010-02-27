from google.appengine.ext import db
import re

from controllers.controller import Controller
from models.user import User

class UserEdit(Controller):
    
    def get(self, userId):
        
        template_values = {}
        
        query = User.all()
        query.filter("id =", userId)
        user = query.get()
        
        template_values['user'] = user
        
        self.output('useredit', 'html', template_values)
    
    def post(self, userId):
        
        user = {}
        user['id'] = userId
        user['name'] = self.request.get('name')
        user['description'] = self.request.get('description')
        user['href'] = self.request.get('href')
        
        errors = {}
        
        from google.appengine.api import users
        currentUser = users.get_current_user()
        if self.getUserId(currentUser.email()) != userId:
            errors['permission'] = True
        
        if len(user['name']) == 0:
            errors['name'] = True
            errors['name_empty'] = True
        if len(user['name']) > 100:
            errors['name'] = True
            errors['name_long'] = True
        
        if len(user['description']) > 5000:
            errors['description'] = True
        
        if not len(user['href']) == 0 and not re.match(r"^https?://.+$", user['href']):
            errors['href'] = True
        
        if errors:
            
            template_values = {
                'user': user,
                'errors': errors
            }
            
            self.output('useredit', 'html', template_values)
            
        else:
            
            query = User.all()
            query.filter("id =", userId)
            userObject = query.get()
            
            userObject.name = user['name']
            userObject.description = user['description']
            userObject.href = user['href']
            userObject.put()
            
            self.redirect('/users/' + userId + '.html')
            

from controllers.controller import Controller

class Badge(Controller):
    def get(self, badge):
        
        from google.appengine.api import users
        user = users.get_current_user()
        if user:
            username = user.email();
        else:
            username = self.request.remote_addr
        
        template_values = {
            'src': self.badges[badge]['src'],
            'name': self.badges[badge]['name'],
            'description': self.badges[badge]['description'],
            'username': self.getUserId(username)
        }
        
        self.output('badge', 'html', template_values)
        

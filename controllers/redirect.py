from controllers.controller import Controller

class Redirect(Controller):
    def get(self, one = None, two = None, three = None):
        
        url = '/'
        
        if self.request.path[0:7] == '/places':
            if self.request.get('loc'):
                url = '/search.html?c=%s' % self.request.get('loc')
            else:
                id = self.request.path[8:40]
                if self.request.path[40:48] == '/history':
                    url = '/attractions/%s/history.html' % id
                elif id:
                    url = '/attractions/%s.html' % id
                else:
                    url = '/search.html'
        elif self.request.path[0:7] == '/m.html' and self.request.get('q'):
            url = '/search.html?q=%s' % self.request.get('q')
        elif self.request.path[0:10] == '/edit.html' and self.request.get('id'):
            url = '/attractions/%s/edit.html' % self.request.get('id')
        
        self.redirect(url)

from controllers.controller import Controller

class Redirect(Controller):
    def get(self, one = None, two = None, three = None):
        
        url = '/'
        if one:
            format = one
        else:
            format = 'html'
        
        if self.request.path[0:7] == '/places':
            if self.request.get('loc'):
                url = '/search.%s?c=%s' % (format, self.request.get('loc'))
            elif self.request.get('lat') and self.request.get('lng') and self.request.get('dlat') and self.request.get('dlng'):
                lat = float(self.request.get('lat')) + (float(self.request.get('dlat')) - float(self.request.get('lat'))) / 2
                lon = float(self.request.get('lng')) + (float(self.request.get('dlng')) - float(self.request.get('lng'))) / 2
                url = '/search.%s?c=%s,%s' % (format, lat, lon)
            elif self.request.get('lat') and self.request.get('lng'):
                url = '/search.%s?c=%s,%s' % (format, self.request.get('lat'), self.request.get('lng'))
            else:
                id = self.request.path[8:40]
                if self.request.path[40:48] == '/history':
                    url = '/attractions/%s/history.%s' % (id, format)
                elif len(id) == 32:
                    url = '/attractions/%s.%s' % (id, format)
                else:
                    url = '/search.%s' % format
        elif self.request.path[0:7] == '/m.html' and self.request.get('q'):
            url = '/search.html?q=%s' % self.request.get('q')
        elif self.request.path[0:10] == '/edit.html' and self.request.get('id'):
            url = '/attractions/%s/edit.html' % self.request.get('id')
        
        self.redirect(url)

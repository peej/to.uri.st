from google.appengine.ext import webapp
import os, re
from google.appengine.ext.webapp import template

class Controller(webapp.RequestHandler):
    
    mimetypes = {
        'html': 'text/html',
        'atom': 'application/atom+xml',
        'js': 'application/javascript'
    }
    
    def output(self, templateName, type = 'html', values = {}):
        
        path = os.path.join(os.path.dirname(__file__), '../templates/' + templateName + '.' + type)
        
        self.response.headers.add_header('Content-type', self.mimetypes[type])
        
        values['page'] = templateName
        values['get'] = {}
        for query in self.request.arguments():
            values['get'][query] = self.request.get(query)
        
        self.response.out.write(template.render(path, values))
        
    def convertFlickrUrl(self, url, type = ''):
        
        if type != '':
            type = '_' + type
        
        url = re.sub(r'^(http://farm[0-9]+\.static\.flickr\.com/[0-9]+/[0-9]+_[0-9a-f]+)(?:_[stmbo])?(\.jpg)$', r'\1' + type + r'\2', url)
        
        return url
        
    def get(self):
        
        path = self.request.path
        if os.path.exists(path):
            self.output(path)
        else:
            path = self.request.path[1:self.request.path.find('.')] + '.html'
            if os.path.exists(path):
                self.output(path)
            else:
                self.output('404', 'html')

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
        
        path = self.request.path[0:self.request.path.find('.')]
        if os.path.exists('templates' + path + '.html'):
            self.output(path, 'html')
        elif os.path.exists('templates' + self.request.path + '.html'):
            self.output(self.request.path, 'html')
        else:
            self.output('404', 'html')
    
    def handle_exception(self, exception, debug_mode):
        super(Controller, self).handle_exception(exception, debug_mode)
        if not debug_mode:
            self.output('500', 'html')

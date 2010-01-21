from google.appengine.ext import webapp
import os
from google.appengine.ext.webapp import template

class Controller(webapp.RequestHandler):
    def output(self, templateName, values, mimetype = 'text/html'):
        
        path = os.path.join(os.path.dirname(__file__), '../templates/' + templateName)
        
        self.response.headers.add_header('Content-type', mimetype)
        
        self.response.out.write(template.render(path, values))
        

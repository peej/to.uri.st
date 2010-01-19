from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from controllers.homepage import HomePage
from controllers.attraction import AttractionPage

application = webapp.WSGIApplication(
    [
        ('/', HomePage),
        ('/attractions/([a-f0-9]{32})(?:\.html)?', AttractionPage)
    ],
    debug=True
)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()


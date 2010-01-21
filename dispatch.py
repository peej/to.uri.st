from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from controllers.homepage import HomePage
from controllers.search import SearchPage
from controllers.attraction import AttractionPage
from controllers.history import HistoryPage

application = webapp.WSGIApplication(
    [
        ('/', HomePage),
        ('/search(?:\.html)?', SearchPage),
        ('/attractions/([a-f0-9]{32})(?:\.html)?', AttractionPage),
        ('/attractions/([a-f0-9]{32})/history(?:\.html)?', HistoryPage)
    ],
    debug=True
)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()


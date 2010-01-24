from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from controllers.homepage import HomePage
from controllers.search import SearchPage
from controllers.attraction import AttractionPage
from controllers.history import HistoryPage
from controllers.edit import EditPage

application = webapp.WSGIApplication(
    [
        ('/', HomePage),
        ('/search(?:\.html)?', SearchPage),
        ('/attractions/([a-f0-9]{32})(?:\.html)?', AttractionPage),
        ('/attractions/([a-f0-9]{32})/history(?:\.html)?', HistoryPage),
        ('/attractions/([a-f0-9]{32})/edit(?:\.html)?', EditPage),
        ('/attractions/add(?:\.html)?', EditPage)
    ],
    debug=True
)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()


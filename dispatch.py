from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from controllers.controller import Controller
from controllers.homepage import HomePage
from controllers.search import SearchPage
from controllers.attraction import AttractionPage
from controllers.history import HistoryPage
from controllers.edit import EditPage
from controllers.recent import RecentPage
from controllers.user import UserPage

application = webapp.WSGIApplication(
    [
        ('/', HomePage),
        ('/search(?:\.(html|atom|js))?', SearchPage),
        ('/attractions/([a-f0-9]{32})(?:\.(html|gpx))?', AttractionPage),
        ('/attractions/([a-f0-9]{32})/history(?:\.html)?', HistoryPage),
        ('/attractions/([a-f0-9]{32})/edit(?:\.html)?', EditPage),
        ('/add(?:\.html)?', EditPage),
        ('/recent(?:\.(html|atom))?', RecentPage),
        ('/users/([a-z0-9-]+)(?:\.html)?', UserPage),
        ('/.*', Controller)
    ],
    debug=True
)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()


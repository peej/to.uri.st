from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from controllers.controller import Controller
from controllers.homepage import HomePage
from controllers.search import SearchPage
from controllers.attraction import AttractionPage
from controllers.history import HistoryPage
from controllers.edit import EditPage
from controllers.comment import CommentAdd
from controllers.recommend import Recommend
from controllers.itinerary import Itinerary
from controllers.recent import RecentPage
from controllers.user import UserPage

application = webapp.WSGIApplication(
    [
        ('/', HomePage),
        ('/search(?:\.(html|atom|js|gpx))?', SearchPage),
        ('/attractions/([a-f0-9]{32})(?:\.(html|gpx))?', AttractionPage),
        ('/attractions/([a-f0-9]{32})/history(?:\.(html|atom))?', HistoryPage),
        ('/attractions/([a-f0-9]{32})/edit(?:\.html)?', EditPage),
        ('/attractions/([a-f0-9]{32})/comment(?:\.html)?', CommentAdd),
        ('/attractions/([a-f0-9]{32})/(?:un)?recommend(?:\.html)?', Recommend),
        ('/attractions/([a-f0-9]{32})/(?:un)?itinerary(?:\.html)?', Itinerary),
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


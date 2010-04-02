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
from controllers.useredit import UserEdit
from controllers.badge import Badge
from controllers.redirect import Redirect

import os
environ = dict(os.environ.items())
if environ['SERVER_SOFTWARE'][0:11] == 'Development':
    debug = True
else:
    debug = False

application = webapp.WSGIApplication(
    [
        ('/', HomePage),
        ('/home(?:\.(html|search|atom))?', HomePage),
        ('/search(?:\.(html|atom|js|gpx|kml))?', SearchPage),
        ('/attractions/([a-f0-9]{32})(?:\.(html|gpx))?', AttractionPage),
        ('/attractions/([a-f0-9]{32})/history(?:\.(html|atom))?', HistoryPage),
        ('/attractions/([a-f0-9]{32})/edit(?:\.html)?', EditPage),
        ('/attractions/([a-f0-9]{32})/comment(?:\.html)?', CommentAdd),
        ('/attractions/([a-f0-9]{32})/(?:un)?recommend(?:\.html)?', Recommend),
        ('/attractions/([a-f0-9]{32})/(?:un)?itinerary(?:\.html)?', Itinerary),
        ('/add(?:\.html)?', EditPage),
        ('/recent(?:\.(html|atom|sitemap|js|kml))?', RecentPage),
        ('/sitemap(?:\.(xml))?', RecentPage),
        ('/users/([a-z0-9-]+)(?:\.(html|atom|js|kml))?', UserPage),
        ('/users/([a-z0-9-]+)/edit(?:\.html)?', UserEdit),
        ('/badges/([0-9]+)(?:\.html)?', Badge),
        
        ('/m\.html', Redirect),
        ('/places(?:\.(html|atom))?', Redirect),
        ('/places/([a-f0-9]{32})(?:\.(html|gpx))?', Redirect),
        ('/places/([a-f0-9]{32})/history(?:\.(html|atom))?', Redirect),
        ('/edit\.html', Redirect),
        
        ('/.*', Controller)
    ],
    debug=debug
)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()


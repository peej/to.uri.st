import datetime
from google.appengine.ext import db
from google.appengine.tools import bulkloader

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.attraction import Attraction

class AttractionLoader(bulkloader.Loader):
    
    def createLocation(self, x):
        parts = x.split(',')
        return db.GeoPt(parts[0], parts[1])
    
    def fixName(self, x):
        if x == '':
            return 'No name'
        else:
            return unicode(x.replace("\n", " "), 'utf-8')
    
    def __init__(self):
        bulkloader.Loader.__init__(self,
            'Attraction',
            [
                ('id', str),
                ('location', self.createLocation),
                ('name', self.fixName),
                ('description', lambda x: unicode(x, 'utf-8')),
                ('href', lambda x: unicode(x, 'utf-8')),
                ('picture', lambda x: unicode(x, 'utf-8')),
                ('region', lambda x: unicode(x, 'utf-8')),
                ('free', lambda x: True if x == 'y' else False),
                ('datetime', lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
            ]
        )

loaders = [AttractionLoader]

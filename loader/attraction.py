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
    
    def __init__(self):
        bulkloader.Loader.__init__(self,
            'Attraction',
            [
                ('id', str),
                ('location', self.createLocation),
                ('name', str),
                ('description', str),
                ('href', lambda x: None if x == '\N' else db.Link(x)),
                ('picture', lambda x: None if x == '\N' else db.Link(x)),
                ('region', str),
                ('free', lambda x: True if x == 'y' else False),
                ('datetime', lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
            ]
        )

loaders = [AttractionLoader]

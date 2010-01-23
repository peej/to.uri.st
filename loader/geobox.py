from google.appengine.ext import db
from google.appengine.tools import bulkloader

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.geobox import GeoBox

class GeoBoxLoader(bulkloader.Loader):
    
    def __init__(self):
        bulkloader.Loader.__init__(self,
            'GeoBox',
            [
                ('lat', float),
                ('lon', float),
                ('attractions', lambda x: x.split(','))
            ]
        )

loaders = [GeoBoxLoader]

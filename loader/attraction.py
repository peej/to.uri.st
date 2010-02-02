import datetime
from google.appengine.ext import db
from google.appengine.tools import bulkloader

import sys, os, re
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
                ('datetime', lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')),
                ('tags', lambda x: [unicode(x, 'utf-8')])
            ]
        )
    
    def handle_entity(self, entity):
        #entity.tags = []
        if '{{dupe}}' in entity.description: entity.tags.append('dupe')
        if '{{delete}}' in entity.description: entity.tags.append('delete')
        if '{{badloc}}' in entity.description: entity.tags.append('badlocation')
        if '{{todo}}' in entity.description: entity.tags.append('todo')
        if '{{trap}}' in entity.description: entity.tags.append('trap')
        if '{{translated}}' in entity.description: entity.tags.append('translated')
        entity.description = re.sub("\{\{[^}]+\}\}", "", entity.description)
        return entity

loaders = [AttractionLoader]

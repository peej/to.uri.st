from google.appengine.ext import db

class Attraction(db.Model):
    id = db.StringProperty()
    root = db.StringProperty()
    previous = db.StringProperty(default = None)
    next = db.StringProperty(default = None)
    location = db.GeoPtProperty(required = True)
    geobox = db.StringProperty()
    name = db.StringProperty(required = True)
    description = db.TextProperty()
    href = db.StringProperty()
    picture = db.StringProperty()
    region = db.StringProperty()
    free = db.BooleanProperty(default = True)
    rating = db.IntegerProperty(default = 0)
    tags = db.StringListProperty()
    userid = db.StringProperty()
    username = db.StringProperty()
    datetime = db.DateTimeProperty(auto_now_add = True)
    
    def __cmp__(self, other):
        return cmp(self.datetime, other.datetime) * -1

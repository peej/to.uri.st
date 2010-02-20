from google.appengine.ext import db

class User(db.Model):
    id = db.StringProperty()
    name = db.StringProperty(required = True)
    location = db.GeoPtProperty()
    description = db.TextProperty()
    href = db.StringProperty()
    favourites = db.StringListProperty()
    recommended = db.StringListProperty()
    itinerary = db.StringListProperty()
    datetime = db.DateTimeProperty(auto_now = True)
    

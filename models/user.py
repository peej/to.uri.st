from google.appengine.ext import db
import dictproperty

class User(db.Model):
    id = db.StringProperty()
    name = db.StringProperty(required = True)
    location = db.GeoPtProperty()
    description = db.TextProperty()
    href = db.StringProperty()
    recommended = db.StringListProperty()
    itinerary = db.StringListProperty()
    stats = dictproperty.DictProperty()
    badges = dictproperty.DictProperty()
    datetime = db.DateTimeProperty(auto_now = True)
    

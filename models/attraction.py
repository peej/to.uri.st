from google.appengine.ext import db

class Attraction(db.Model):
    id = db.StringProperty()
    previous = db.StringProperty(default = None)
    next = db.StringProperty(default = None)
    location = db.GeoPtProperty(required = True)
    name = db.StringProperty(required = True)
    description = db.TextProperty()
    href = db.LinkProperty()
    picture = db.LinkProperty()
    region = db.StringProperty()
    free = db.BooleanProperty(default = True)
    rating = db.RatingProperty()
    user = db.UserProperty()
    datetime = db.DateTimeProperty()

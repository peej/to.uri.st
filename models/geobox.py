from google.appengine.ext import db

class GeoBox(db.Model):
    lat = db.FloatProperty()
    lon = db.FloatProperty()
    attractions = db.StringListProperty()

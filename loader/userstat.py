from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from models.user import User

class UserStat(webapp.RequestHandler):
    def get(self):
        userid = self.request.get('u')
        
        query = User.all()
        query.filter("id =", userid)
        userObject = query.get()
        
        if userObject:
            
            self.response.out.write("<pre>")
            self.response.out.write("Username: %s\n" % userObject.username)
            self.response.out.write("Name: %s\n" % userObject.name)
            self.response.out.write(userObject.stats)
            self.response.out.write("\n")
            self.response.out.write(userObject.badges)
            self.response.out.write("\n")
            
def main():
    run_wsgi_app(webapp.WSGIApplication([
        ('/userstat', UserStat),
    ]))

if __name__ == '__main__':
    main()

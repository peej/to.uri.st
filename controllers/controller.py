from google.appengine.ext import webapp
import os, re
from google.appengine.ext.webapp import template

class Controller(webapp.RequestHandler):
    
    mimetypes = {
        'html': 'text/html',
        'atom': 'application/atom+xml',
        'js': 'application/javascript',
        'gpx': 'application/gpx+xml'
    }
    
    tags = {
        'nature': 'nature',
        'wildlife': 'wildlife',
        'beach': 'beach',
        'beaches': 'beach',
        'lake': 'lake',
        'lakes': 'lake',
        'wetland': 'wetland',
        'forest': 'forest',
        'forests': 'forest',
        'waterfall': 'waterfall',
        'waterfalls': 'waterfall',
        'castle': 'castle',
        'castles': 'castle',
        'palace': 'palace',
        'palaces': 'palace',
        'citywalls': 'citywalls',
        'citywall': 'citywalls',
        'tower': 'tower',
        'towers': 'tower',
        'ruins': 'ruins',
        'ruin': 'ruins',
        'church': 'church',
        'churches': 'church',
        'farm': 'farm',
        'farms': 'farm',
        'windmill': 'windmill',
        'windmills': 'windmill',
        'vineyard': 'vineyard',
        'vineyards': 'vineyard',
        'winery': 'vineyard',
        'wineries': 'vineyard',
        'watermill': 'watermill',
        'watermills': 'watermill',
        'garden': 'garden',
        'gardens': 'garden',
        'bridge': 'bridge',
        'bridges': 'bridge',
        'fountain': 'fountain',
        'fountains': 'fountain',
        'monument': 'monument',
        'monuments': 'monument',
        'worldheritagesite': 'worldheritagesite',
        'worldheritagesites': 'worldheritagesite',
        'statue': 'statue',
        'statues': 'statue',
        'park': 'park',
        'parks': 'park',
        'picnic': 'picnic',
        'picnicsite': 'picnic',
        'picnicsites': 'picnic',
        'picnicarea': 'picnic',
        'picnicareas': 'picnic',
        'view': 'view',
        'views': 'view',
        'cave': 'cave',
        'caves': 'cave',
        'shop': 'shop',
        'shops': 'shop',
        'bookshop': 'bookshop',
        'bookshops': 'bookshop',
        'giftshop': 'giftshop',
        'giftshops': 'giftshop',
        'artgallery': 'artgallery',
        'artgalleries': 'artgallery',
        'market': 'market',
        'markets': 'market',
        'bowling': 'bowling',
        'snooker': 'snooker',
        'snookerhall': 'snooker',
        'snookerhalls': 'snooker',
        'billiard': 'snooker',
        'billiards': 'snooker',
        'billiardhall': 'snooker',
        'billiardhalls': 'snooker',
        'aquarium': 'aquarium',
        'aquaria': 'aquarium',
        'aquariums': 'aquarium',
        'cinema': 'cinema',
        'cinemas': 'cinema',
        'theatre': 'theatre',
        'theater': 'theatre',
        'theatres': 'theatre',
        'theaters': 'theatre',
        'casino': 'casino',
        'casinos': 'casino',
        'music': 'music',
        'historic': 'historic',
        'historicsite': 'historic',
        'history': 'historic',
        'archeological': 'archeological',
        'archeology': 'archeological',
        'naval': 'naval',
        'navalmuseum': 'naval',
        'war': 'war',
        'warmuseum': 'war',
        'science': 'science',
        'sciencemuseum': 'science',
        'crafts': 'crafts',
        'craft': 'crafts',
        'museum': 'museum',
        'museums': 'museum',
        'themepark': 'themepark',
        'themeparks': 'themepark',
        'rollercoaster': 'themepark',
        'rollercoasters': 'themepark',
        'zoo': 'zoo',
        'zoos': 'zoo',
        'zoologicalgarden': 'zoo',
        'zoologicalgardens': 'zoo',
        'animalpark': 'zoo',
        'animalparks': 'zoo',
        'art': 'art',
        'artgallery': 'art',
        'artgalleries': 'art',
        'circus': 'circus',
        'circuses': 'circus',
        'festival': 'festival',
        'festivals': 'festival',
        'waterpark': 'waterpark',
        'waterparks': 'waterpark',
        'ferriswheel': 'ferriswheel',
        'ferriswheels': 'ferriswheel',
        'bigwheel': 'ferriswheel',
        'bigwheels': 'ferriswheel',
        'playground': 'playground',
        'playgrounds': 'playground',
        'bar': 'bar',
        'bars': 'bar',
        'cafe': 'cafe',
        'cafes': 'cafe',
        'icecream': 'icecream',
        'icecreamparlour': 'icecream',
        'icecreamparlours': 'icecream',
        'icecreamshop': 'icecream',
        'icecreamshops': 'icecream',
        'sport': 'sport',
        'sports': 'sport',
        'stadium': 'stadium',
        'stadiums': 'stadium',
        'americanfootball': 'americanfootball',
        'americanfootballstadium': 'americanfootball',
        'americanfootballstadiums': 'americanfootball',
        'americanfootballpitch': 'americanfootball',
        'americanfootballpitches': 'americanfootball',
        'baseball': 'baseball',
        'baseballstadium': 'baseball',
        'baseballstadiums': 'baseball',
        'baseballpitch': 'baseball',
        'baseballpitches': 'baseball',
        'basketball': 'basketball',
        'basketballstadium': 'basketball',
        'basketballstadiums': 'basketball',
        'cricket': 'cricket',
        'cricketstadium': 'cricket',
        'cricketgreen': 'cricket',
        'cricketgreens': 'cricket',
        'cricketpitch': 'cricket',
        'cricketpitches': 'cricket',
        'football': 'football',
        'footballstadium': 'football',
        'footballstadiums': 'football',
        'footballpitch': 'football',
        'footballpitches': 'football',
        'golf': 'golf',
        'golfcourse': 'golf',
        'golfcourses': 'golf',
        'rugby': 'rugby',
        'rugbystadium': 'rugby',
        'rugbystadiums': 'rugby',
        'rugbypitch': 'rugby',
        'rugbypitches': 'rugby',
        'tennis': 'tennis',
        'tenniscourt': 'tennis',
        'tenniscourts': 'tennis',
        'cycling': 'cycling',
        'racetrack': 'racetrack',
        'motorracing': 'racetrack',
        'speedway': 'racetrack',
        'archery': 'archery',
        'climbing': 'climbing',
        'rockclimbing': 'climbing',
        'fishing': 'fishing',
        'fish': 'fishing',
        'hiking': 'hiking',
        'hike': 'hiking',
        'hikes': 'hiking',
        'horse': 'horse',
        'horseracing': "horse",
        'horseracingtrack': "horse",
        'horseracingtracks': "horse",
        'skateboarding': 'skateboarding',
        'skatepark': 'skateboarding',
        'skateparks': 'skateboarding',
        'pool': 'pool',
        'pools': 'pool',
        'swimmingpool': 'pool',
        'swimmingpools': 'pool',
        'kayaking': 'kayaking',
        'boating': 'boating',
        'boat': 'boating',
        'boats': 'boating',
        'surfing': 'surfing',
        'surf': 'surfing',
        'swimming': 'swimming',
        'swim': 'swimming',
        'waterski': 'waterski',
        'waterskiing': 'waterski',
        'windsurf': 'windsurf',
        'windsurfing': 'windsurf',
        'icehockey': 'icehockey',
        'iceskating': 'iceskating',
        'iceskate': 'iceskating',
        'icerink': 'iceskating',
        'icerinks': 'iceskating',
        'skiing': 'skiing',
        'ski': 'skiing',
        'skislope': 'skiing',
        'snowboarding': 'snowboarding'
    }
    
    def output(self, templateName, type = 'html', values = {}):
        
        path = os.path.join(os.path.dirname(__file__), '../templates/' + templateName + '.' + type)
        
        if self.request.get('pretty'):
            self.response.headers.add_header('Content-type', 'text/plain')
        else:
            self.response.headers.add_header('Content-type', self.mimetypes[type])
        
        values['page'] = templateName
        values['get'] = {}
        for query in self.request.arguments():
            values['get'][query] = self.request.get(query)
        
        #self.response.headers.add_header('Cache-control', 'no-cache')
        
        from google.appengine.api import users
        user = users.get_current_user()
        if user:
            values['signedin'] = {
                'userid': user.email().replace('@', '-').replace('.', '-'),
                'nickname': user.nickname(),
                'signout': users.create_logout_url("/")
            }
        
        self.response.out.write(template.render(path, values))
        
    def convertFlickrUrl(self, url, type = ''):
        
        if type != '':
            type = '_' + type
        
        url = re.sub(r'^(http://farm[0-9]+\.static\.flickr\.com/[0-9]+/[0-9]+_[0-9a-f]+)(?:_[stmbo])?(\.jpg)$', r'\1' + type + r'\2', url)
        
        return url
        
    def getUserId(self, user):
        if user:
            return user.email().replace('@', '-').replace('.', '-')
    
    def getUserObject(self, user):
        
        from google.appengine.api import users
        from models.user import User
        
        if type(user) == users.User:
            userId = self.getUserId(user)
        else:
            userId = user
        
        query = User.all()
        query.filter("id =", userId)
        userObject = query.get()
        
        if userObject == None and type(user) == users.User:
            userObject = User(
                id = userId,
                name = user.nickname()
            )
            userObject.put()
        
        return userObject
    
    def get(self):
        
        path = self.request.path[1:self.request.path.find('.')]
        if os.path.exists('templates/' + path + '.html'):
            self.output(path, 'html')
        elif os.path.exists('templates' + self.request.path + '.html'):
            self.output(self.request.path[1:], 'html')
        else:
            self.error(404)
            self.output('404', 'html')
    
    def handle_exception(self, exception, debug_mode):
        super(Controller, self).handle_exception(exception, debug_mode)
        if not debug_mode:
            self.error(500)
            self.output('500', 'html')

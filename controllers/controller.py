from google.appengine.ext import webapp
import os, re
from google.appengine.ext.webapp import template

class Controller(webapp.RequestHandler):
    
    mimetypes = {
        'html': 'text/html',
        'atom': 'application/atom+xml',
        'js': 'application/javascript',
        'gpx': 'application/gpx+xml',
        'kml': 'application/vnd.google-earth.kml+xml'
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
    
    badges = {
        '1': {
            'src': '/_/badges/1.png',
            'name': 'Newbie',
            'description': 'You\'ve edited your first attraction'
        },
        '2': {
            'src': '/_/badges/2.png',
            'name': 'Tripple wammy',
            'description': 'You\'re 3rd edit is in the bag'
        },
        '3': {
            'src': '/_/badges/3.png',
            'name': 'Day tripper',
            'description': '10 attractions updated'
        },
        '4': {
            'src': '/_/badges/4.png',
            'name': 'Know it all',
            'description': '25 attractions updated'
        },
        '5': {
            'src': '/_/badges/5.png',
            'name': 'Superstar',
            'description': 'Wow! You\'ve hit the ton, 100 attractions updated'
        },
        '6': {
            'src': '/_/badges/6.png',
            'name': 'Local',
            'description': 'Keeping it local, you\'ve edited 5 attractions in the same neighbourhood'
        },
        '7': {
            'src': '/_/badges/7.png',
            'name': 'Native',
            'description': 'You\'re putting down roots, 20 edits in one neighbourhood'
        },
        '8': {
            'src': '/_/badges/8.png',
            'name': 'Advocate',
            'description': 'Someone has recommended an attraction you\'ve edited'
        },
        '9': {
            'src': '/_/badges/9.png',
            'name': 'Trendsetter',
            'description': 'You\'re attractions have gained a following, 5 people have recommended them'
        },
        '10': {
            'src': '/_/badges/10.png',
            'name': 'Tour guide',
            'description': 'Wow, everyone loves the attractions you\'ve edited, 25 recommendations'
        },
        '11': {
            'src': '/_/badges/11.png',
            'name': 'A thousand words',
            'description': 'A picture tells a thousand words, or so they say'
        },
        '12': {
            'src': '/_/badges/12.png',
            'name': 'Shutterbug',
            'description': 'You\'re a photo finding hero'
        },
        '13': {
            'src': '/_/badges/13.png',
            'name': 'Dead ringer',
            'description': 'Thanks for identifying 3 duplicate attractions'
        },
        '14': {
            'src': '/_/badges/14.png',
            'name': 'Commentator',
            'description': 'Congratulations on your first comment'
        },
        '15': {
            'src': '/_/badges/15.png',
            'name': 'Gossip',
            'description': 'Keep spreading the love with your words of wisdom'
        },
        '16': {
            'src': '/_/badges/16.png',
            'name': 'Motormouth',
            'description': 'Give your mouth a rest, that\'s 25 comments'
        }
    }
    
    def output(self, templateName, type = 'html', values = {}):
        
        path = os.path.join(os.path.dirname(__file__), '../templates/' + templateName + '.' + type)
        
        if not os.path.exists(path):
            self.send404()
            return
        
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
                'signout': users.create_logout_url(self.request.path)
            }
        else:
            values['signedout'] = {
                'ip': self.request.remote_addr,
                'signin': users.create_login_url(self.request.path)
            }
        
        self.response.out.write(template.render(path, values))
        
    def convertFlickrUrl(self, url, type = ''):
        
        if type != '':
            type = '_' + type
        
        url = re.sub(r'^(http://farm[0-9]+\.static\.flickr\.com/[0-9]+/[0-9]+_[0-9a-f]+)(?:_[stmbo])?(\.jpg)$', r'\1' + type + r'\2', url)
        
        return url
        
    def getUserId(self, user):
        from google.appengine.api import users
        
        if type(user) == users.User:
            email = user.email()
        elif type(user) == unicode or type(user) == str:
            email = user
        else:
            email = ''
        
        return email.replace('@', '-').replace('.', '-')
    
    def getUserObject(self, user = None):
        
        from google.appengine.api import users
        from models.user import User
        
        if user == None:
            user = users.get_current_user()
        
        userId = self.getUserId(user)
        
        query = User.all()
        query.filter("id =", userId)
        userObject = query.get()
        
        if userObject == None:
            if type(user) == users.User:
                userObject = User(
                    id = userId,
                    name = user.nickname()
                )
            else:
                userObject = User(
                    id = userId,
                    name = user
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
            self.send404()
    
    def send404(self):
        self.error(404)
        self.output('404', 'html')
        self.sendAdminMail('404')
    
    def handle_exception(self, exception, debug_mode):
        super(Controller, self).handle_exception(exception, debug_mode)
        if not debug_mode:
            self.error(500)
            self.output('500', 'html')
        self.sendAdminMail('500')
    
    def sendAdminMail(self, errType):
        from google.appengine.api import users
        from google.appengine.api import mail
        
        user = users.get_current_user()
        if user:
            sender = user.email()
        else:
            sender = "peejeh@gmail.com"
        
        to = "support@to.uri.st"
        subject = errType + " error"
        body = self.request.path
        mail.send_mail(sender, to, subject, body)
    
    def addStat(self, user, id, subId = None):
        if subId == None:
            try:
                user.stats[id] = user.stats[id] + 1
            except:
                user.stats[id] = 1
        else:
            try:
                user.stats[id][subId] = user.stats[id][subId] + 1
            except:
                try:
                    user.stats[id][subId] = 1
                except:
                    user.stats[id] = {}
                    user.stats[id][subId] = 1
    
    def updateBadges(self, user):
        from datetime import datetime
        
        oldBadges = user.badges.copy()
        
        # edits
        try:
            if user.stats[1] >= 100 and not 5 in user.badges:
                user.badges[5] = datetime.today()
            elif user.stats[1] >= 25 and not 4 in user.badges:
                user.badges[4] = datetime.today()
            elif user.stats[1] >= 10 and not 3 in user.badges:
                user.badges[3] = datetime.today()
            elif user.stats[1] >= 3 and not 2 in user.badges:
                user.badges[2] = datetime.today()
            elif user.stats[1] >= 1 and not 1 in user.badges:
                user.badges[1] = datetime.today()
        except:
            pass
        
        # local edits
        try:
            for loc in user.stats[2]:
                if user.stats[2][loc] >= 20 and not 7 in user.badges:
                    user.badges[7] = datetime.today()
                elif user.stats[2][loc] >= 5 and not 6 in user.badges:
                    user.badges[6] = datetime.today()
        except:
            pass
        
        # recommended
        try:
            if user.stats[3] >= 25 and not 10 in user.badges:
                user.badges[10] = datetime.today()
            elif user.stats[3] >= 5 and not 9 in user.badges:
                user.badges[9] = datetime.today()
            elif user.stats[3] >= 1 and not 8 in user.badges:
                user.badges[8] = datetime.today()
        except:
            pass
        
        # comments
        try:
            if user.stats[6] >= 25 and not 16 in user.badges:
                user.badges[16] = datetime.today()
            elif user.stats[6] >= 5 and not 15 in user.badges:
                user.badges[15] = datetime.today()
            elif user.stats[6] >= 1 and not 14 in user.badges:
                user.badges[14] = datetime.today()
        except:
            pass
        
        return [val for val in user.badges if val not in oldBadges]

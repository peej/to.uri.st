from google.appengine.api.labs import taskqueue
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from models.attraction import Attraction

class AutoTagWorker(webapp.RequestHandler):
    
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
    
    def get(self):
        n = self.request.get('n') or 1
        f = self.request.get('f') or 1
        
        taskqueue.add(
            url = '/autotag',
            params = {
                'n': n,
                'f': f
            }
        )
        
        self.response.out.write("running")
    
    def post(self):
        n = int(self.request.get('n'))
        l = 50
        f = self.request.get('f')
        
        import csv
        
        csvReader = csv.reader(open('attractions' + f + '.csv'))
        
        count = 1
        for row in csvReader:
            
            if count >= n and count < n + l:
                
                query = Attraction.all()
                query.filter("id =", row[0])
                attraction = query.get()
                
                if attraction:
                    if row[9] != '' and row[9] != 'unknown' and row[9] not in attraction.tags:
                        attraction.tags.append(row[9])
                    for key in self.tags.keys():
                        if ' ' + key + ' ' in ' ' + row[3].lower() + ' ' and self.tags[key] not in attraction.tags:
                            attraction.tags.append(self.tags[key])
                    if 'unknown' in attraction.tags:
                        attraction.tags.remove('unknown')
                    attraction.put()
                
            elif count >= n:
                
                taskqueue.add(
                    url = '/autotag',
                    params = {
                        'n': n + l,
                        'f': f
                    }
                )
                break
            
            count = count  + 1
        
def main():
    run_wsgi_app(webapp.WSGIApplication([
        ('/autotag', AutoTagWorker),
    ]))

if __name__ == '__main__':
    main()

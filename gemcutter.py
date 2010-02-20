import urllib2
# we should use simplejson from django.utils
from django.utils import simplejson
#import simplejson


GEMCUTTER_API_URL = "http://gemcutter.org/api/v1/"
API_KEY_URL = GEMCUTTER_API_URL + "api_key"
GEMS_URL = GEMCUTTER_API_URL + 'gems/'
GEM_SEARCH_URL = GEMCUTTER_API_URL + 'search.json?query='

class Gem(object):
    def __init__(self, jsoned_gem, format='json'):
        if format == 'raw':
            self.values = jsoned_gem
        else:
            self.values = simplejson.loads(jsoned_gem)
    def __str__(self): 
        return str(self.values)
    #todo dependencies
    
class Gemcutter(object):
        
    def authenticate(self, _email, _password):
        self.email = _email
        self.password = _password    
        auth_handler = urllib2.HTTPBasicAuthHandler()
        auth_handler.add_password(realm='Application',
            uri=API_KEY_URL,
            user=self.email,
            passwd=self.password)
        opener = urllib2.build_opener(auth_handler)
        urllib2.install_opener(opener)        
        try:
          f = urllib2.urlopen(API_KEY_URL)
          return True
        except:
          return False
                
    def api_key(self):         
        try:
          f = urllib2.urlopen(API_KEY_URL)
          api_key = f.read(1024)
          return api_key
        except:
          return None
          
    def gem(self, gem_name):
        try:
            f = urllib2.urlopen(GEMS_URL+gem_name+'.json')
            gem_info = f.read(40000)
            return Gem(gem_info)             
        except:
            return None
   
    def search(self, gem_name, idx=0):
        try:
            f = urllib2.urlopen(GEM_SEARCH_URL+gem_name)
            gem_info = simplejson.loads(f.read(40000))
            if len(gem_info) > 1:
                return len(gem_info)
            else:
                if idx > len(gem_info) - 1:
                    return None
                else:                    
                    return Gem(simplejson.loads(gem_info)[idx], 'raw')            
        except:
            return None

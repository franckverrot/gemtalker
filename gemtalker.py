import cgi
from gemcutter import *
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.api import xmpp
from google.appengine.ext.webapp.util import run_wsgi_app



class User(db.Model):
    email = db.TextProperty()
    api_key = db.TextProperty()
    received_at = db.DateTimeProperty(auto_now_add=True)

class Log(db.Model):
    email = db.TextProperty()
    content = db.TextProperty()
    received_at = db.DateTimeProperty(auto_now_add=True)
          
class MainPage(webapp.RequestHandler):
    def get(self):
        self.response.out.write("""
          <html>
          <head>
            <title>Welcome to Gemtalker!</title>
          </head>
            <body>
                <h1>Welcome to Gemtalker!</h1>
                <p>Invite gemtalker@appspot.com in Google Talk and let's have a little chat (you can say "help" to get started)</p>
                <h2>F.A.Q</h2>
                
                <h3><a name="#AUTH">AUTH</a></h3>
                <p>
                By using the AUTH command you allow gemtalker to use your API key to talk to Gemcutter's REST API.<br />
                We won't use that key unless you're talking to the bot but if you want to, you can reset it in your profile's panel at <a href="http://gemcutter.org/profile">Gemcutter's</a>.<br />
                Usage: <i><b>AUTH</b> myemailadress:mypassword</i>
                <br />
                IMPORTANT: We do not store passwords, we only cache API key!
                </p>
                
                
            </body>
          <html>""")


class XMPPHandler(webapp.RequestHandler):
    def post(self):
        message = xmpp.Message(self.request.POST)
        email = cgi.escape(self.request.get('from')).split("/")[0]
        body = message.body
        log = Log()
        log.email = email
        log.content = body
        log.put()
        #user_api_key = None
        user = 1
        #user = db.GqlQuery("SELECT email, api_key FROM User WHERE email like "+email+" LIMIT 1")
        if user == None:
            user = User()
            user.email = email
            user.put()
            message.reply("Hello %(email)s, type \"help\" for help!" % { 'email' : user.email })
        
        user_input = body.decode('ascii','replace').split()
        command = user_input.pop(0)

        if command == "help":
            message.reply("Visit http://gemtalker.appspot.com/")
        elif command == "search":
            message.reply("Search not implemented yet")
        elif command == "info":
            if len(user_input) == 0: #only command...
                message.reply("Usage: _*info* gemname [info={name, version, authors, ...}]_")
            elif len(user_input) == 1: #only command and gem
                try:            
                    gem = Gemcutter().gem(str(user_input[0]))
                    message.reply("Available info: %(methods)s" % { 'methods' : str(gem.values.keys()) })
                except:
                    message.reply("Gem %(gem)s does not exist." % { 'gem' : str(user_input[0]) })
            elif len(user_input) == 2:
                attr = user_input[1].decode('ascii','replace')
                try:            
                    gem = Gemcutter().gem(str(user_input[0]))

                    if attr in gem.values.keys():
                        message.reply(str(gem.values[user_input[1]]))
                    else:
                        message.reply("The information %(info)s cannot be found for the gem %(gem)s. Try : %(methods)s." % { 'info' : attr, 'gem' : user_input[0], 'methods' : str(gem.values.keys()) })              
                    #message.reply(str(gem.__getattribute__(user_input[1])()))
                except Exception, e:
                    message.reply("Gem %(gem)s does not exist... %(e)s" % { 'gem' : user_input[0], 'e' : str(e) })

            else: 
                    message.reply("If you're not sure what you doing : http://gemtalker.appspot.com/ because I can't understand "+command+" "+str(user_input))     
        else:
            message.reply("I can't understand "+command)
                    
        #if user_api_key == None:
        #    if body.split()[0] != "AUTH":
        #        message.reply("Hello! First, please send your Gemcutter's login and password separated by ':' and prefixed by the 'AUTH' command. eg: AUTH xyz@domain.com:mypassword. (If you're not sure what you doing : http://gemtalker.appspot.com/#AUTH)")
        #    else:
       #         message.reply("oki")
                
        
#=======================================================================
# WGSI application below
#=======================================================================
application = webapp.WSGIApplication( [
                                            ('/', MainPage), 
                                            ('/_ah/xmpp/message/chat/', XMPPHandler)
                                       ],
                                       debug=True)
def main():
    run_wsgi_app(application)
 
if __name__ == "__main__":
    main()

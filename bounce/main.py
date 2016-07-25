import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb
import jinja2
import os

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))

class Idea(ndb.Model):
    text = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    details = ndb.StringProperty()
    references = ndb.StringProperty()

class HomeHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('home.html')
        self.response.write(template.render())

class CreateHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('create.html')
        self.response.write(template.render())

class IdeaHandler(webapp2.RequestHandler):
    def get(self):

        ideas = Idea.query().order(Idea.idea).fetch()

        template_values = {'ideas':ideas}
        template = jinja_environment.get_template('idea.html')
        self.response.write(template.render(template_values))

    def post(self):

        idea = self.request.get('idea')
        username = users.get_current_user().email()

        new_idea = Idea(text=idea, email=username)

        new_idea.put()

        ideas = Idea.query().fetch()
        template_values = {'ideas':ideas}
        template = jinja_environment.get_template('idea.html')
        self.response.write(template.render(template_values))

        self.redirect('/')

app = webapp2.WSGIApplication([
    ('/', HomeHandler),
    ('/create', CreateHandler),
    ('/idea', IdeaHandler)
], debug=True)

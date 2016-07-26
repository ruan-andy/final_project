import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb
import jinja2
import os

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))

class Idea(ndb.Model):
    title = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    text = ndb.StringProperty()
    reference = ndb.StringProperty()
    def url(self):
        return '/idea?key=' + self.key.urlsafe()

class Comment(ndb.Model):
    name = ndb.StringProperty()
    text = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    #post_key = ndb.KeyProperty(kind = Post)

class HomeHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('home.html')
        self.response.write(template.render())

class IdeaHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('create.html')
        self.response.write(template.render())


class CreateHandler(webapp2.RequestHandler):
    def get(self):

        #ideas = Idea.query().order(Idea.idea).fetch()

        #template_values = {'ideas':ideas}
        template = jinja_environment.get_template('createidea.html')
        self.response.write(template.render())

    def post(self):

        idea = self.request.get('idea')
        username = users.get_current_user().email()

        new_idea = Idea(text=idea, email=username)

        new_idea.put()

        ideas = Idea.query().fetch()
        template_values = {'ideas':ideas}
        template = jinja_environment.get_template('idea.html')
        self.response.write(template.render(template_values))

        self.redirect('/idea')

app = webapp2.WSGIApplication([
    ('/', HomeHandler),
    ('/create', CreateHandler),
    ('/idea', IdeaHandler)
], debug=True)

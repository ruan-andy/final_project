import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb
import jinja2
import os
import logging

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))

class Idea(ndb.Model):
    name = ndb.StringProperty()
    text = ndb.StringProperty()
    title = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    reference = ndb.StringProperty()
    def url(self):
        return '/idea?key=' + self.key.urlsafe()

class HomeHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            nickname = user.nickname()
            logout_url = users.create_logout_url('/')
            greeting = 'Welcome, {}! (<a href="{}">sign out</a>)'.format(
                nickname, logout_url)
        else:
            login_url = users.create_login_url('/')
            greeting = '<a href="{}">Sign in</a>'.format(login_url)

        self.response.write('<html><body>{}</body></html>'.format(greeting))

        template = jinja_environment.get_template('home.html')
        self.response.write(template.render())

class IdeaHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('idea.html')
        self.response.write(template.render())

    def post(self):
        # get request
        name = self.request.get('name')
        text = self.request.get('text')
        # logic
        idea = Idea(name=name, text=text, )
        idea.put()
        # render
        self.redirect('/idea')

        ideas = Idea.query().fetch()
        template_values = {'ideas':ideas}
        template = jinja_environment.get_template('createidea.html')
        self.response.write(template.render(template_values))

class CreateHandler(webapp2.RequestHandler):
    def get(self):

        #ideas = Idea.query().order(Idea.idea).fetch()

        #template_values = {'ideas':ideas}
        template = jinja_environment.get_template('createidea.html')
        self.response.write(template.render())

    def post(self):
        title = self.request.get('title')
        text = self.request.get('text')
        reference = self.request.get('reference')
        name = users.get_current_user().email()

        new_idea = Idea(title=title, text=text, refernece = reference)

        new_idea.put()

        self.redirect('/')

app = webapp2.WSGIApplication([
    ('/', HomeHandler),
    ('/create', CreateHandler),
    ('/idea', IdeaHandler)
], debug=True)

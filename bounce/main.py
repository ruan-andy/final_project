import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb
import jinja2
import os
import logging

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))

class Tree(ndb.Model):
    title = ndb.StringProperty()
    name = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    def url(self):
        return '/index?key=' + self.key.urlsafe()

class Idea(ndb.Model):
    title = ndb.StringProperty()
    text = ndb.StringProperty()
    description = ndb.StringProperty()
    name = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    reference = ndb.StringProperty()
    tree_key = ndb.KeyProperty(kind=Tree)
    def url(self):
        return '/idea?key=' + self.key.urlsafe()

class Comment(ndb.Model):
    name = ndb.StringProperty()
    text = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    idea_key = ndb.KeyProperty(kind=Idea)

class UserHandler(webapp2.RequestHandler):
    def get(self):
        name = users.get_current_user().email()
        ideas = Idea.query(Idea.name == name).fetch()
        template_values = {'ideas': ideas}
        template = jinja_environment.get_template('list.html')
        self.response.write(template.render(template_values))

class SignInHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('signin.html')
        self.response.write(template.render())

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

class CreateHandler(webapp2.RequestHandler):
    def get(self):
        #ideas = Idea.query().order(Idea.idea).fetch()

        #template_values = {'ideas':ideas}
        key = self.request.get('key')
        template_values = {'key':key}
        template = jinja_environment.get_template('createidea.html')
        self.response.write(template.render(template_values))

    def post(self):
        title = self.request.get('title')
        text = self.request.get('text')
        description = self.request.get('description')
        reference = self.request.get('reference')
        name = users.get_current_user().email()

        urlsafe_key = self.request.get('key')
        if urlsafe_key == "":
            new_tree = Tree(title=title, name=name)
            new_tree.put()
            tree_key = new_tree.key
        else:
            tree_key = ndb.Key(urlsafe = urlsafe_key)
            #tree_key = key.get()

        new_idea = Idea(title=title, text=text, description=description, name=name, reference=reference, tree_key=tree_key)
        new_idea.put()

        self.redirect(tree_key.get().url())


class IdeaHandler(webapp2.RequestHandler):
    def get(self):
        # get info
        urlsafe_key = self.request.get('key')
        #logic
        key = ndb.Key(urlsafe = urlsafe_key)
        idea = key.get()
        comments = Comment.query(Comment.idea_key == idea.key).order(Comment.date).fetch()
        # render
        template_values = {'idea': idea, 'comments': comments}
        template = jinja_environment.get_template('idea.html')
        self.response.write(template.render(template_values))

    def post(self):
        # get request
        name = users.get_current_user().email()
        text = self.request.get('text')
        idea_key_urlsafe = self.request.get('key')
        # logic
        idea_key = ndb.Key(urlsafe=idea_key_urlsafe)
        idea = idea_key.get()

        comment = Comment(name=name, text=text, idea_key=idea.key)
        comment.put()
        # render
        self.redirect(idea.url())

class ListHandler(webapp2.RequestHandler):
    def get(self):
        urlsafe_key = self.request.get('key')
        key = ndb.Key(urlsafe = urlsafe_key)
        tree = key.get()
        ideas = Idea.query(Idea.tree_key == tree.key).fetch()
        template_values = {'ideas': ideas}
        template = jinja_environment.get_template('list.html')
        self.response.write(template.render(template_values))

class IndexHandler(webapp2.RequestHandler):
    def get(self):
        #---------------------
        urlsafe_key = self.request.get('key')
        key = ndb.Key(urlsafe = urlsafe_key)
        tree = key.get()
        tmp = Idea.query(Idea.tree_key == tree.key).fetch()
        ideas = sorted(tmp, key=lambda k: k.date )
        #---------------
        #ideas = Idea.query().fetch()
        template_values = {'ideas': ideas, 'key':urlsafe_key}
        template = jinja_environment.get_template('index.html')
        self.response.write(template.render(template_values))

class TreeHandler(webapp2.RequestHandler):
    def get(self):
        trees = Tree.query().fetch()
        template_values = {'trees':trees}
        template = jinja_environment.get_template('treelist.html')
        self.response.write(template.render(template_values))

    # def post(self):
    #     title = self.request.get('title')
    #     name = users.get_current_user().email()
    #
    #     new_tree = Tree(title=title, name=name)
    #
    #     new_tree.put()
    #
    #     self.redirect('/tree')

class UpdateHandler(webapp2.RequestHandler):
    def get(self):
        #ideas = Idea.query().order(Idea.idea).fetch()

        #template_values = {'ideas':ideas}
        key = self.request.get('key')
        template_values = {'key':key}
        template = jinja_environment.get_template('update.html')
        self.response.write(template.render(template_values))

    def post(self):
        title = self.request.get('title')
        text = self.request.get('text')
        description = self.request.get('description')
        reference = self.request.get('reference')
        name = users.get_current_user().email()

        urlsafe_key = self.request.get('key')
        if urlsafe_key == "":
            new_tree = Tree(title=title, name=name)
            new_tree.put()
            tree_key = new_tree.key
        else:
            tree_key = ndb.Key(urlsafe = urlsafe_key)
            #tree_key = key.get()

        new_idea = Idea(title=title, text=text, description=description, name=name, reference=reference, tree_key=tree_key)
        new_idea.put()

        self.redirect('/treelist')

app = webapp2.WSGIApplication([
    ('/ulist', UserHandler),
    ('/signin', HomeHandler),
    ('/', SignInHandler),
    ('/create', CreateHandler),
    ('/idea', IdeaHandler),
    ('/list', ListHandler),
    ('/treelist', TreeHandler),
    ('/index', IndexHandler),
    ('/update', UpdateHandler)
], debug=True)

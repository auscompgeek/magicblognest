import urllib
import webapp2

import jinja2
import os

import datetime

from google.appengine.ext import db
import cgi

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MainPage(webapp2.RequestHandler):
  def get(self):
    """Handle GET requests to the root."""

    template_values = {
      'posts': BlogPost.all().order('-date'),
      'time': datetime.datetime.now(),
    }

    template = jinja_environment.get_template('index.html')
    self.response.out.write(template.render(template_values))

class NewFormPage(webapp2.RequestHandler):
  def get(self):
    """Handle GET requests for the new post form."""

    template_values = {}
    template = jinja_environment.get_template('new.html')
    self.response.out.write(template.render(template_values))

class NewSubmitPage(webapp2.RequestHandler):
  def post(self):
    """Handle new post submissions."""

    text_content = self.request.get('text').strip()
    heading = self.request.get('heading').strip()
    author = self.request.get('author').strip()
    post_type = self.request.get('type')

    if post_type == 'html' and not author:
      raise Exception('cannot post anon html')

    heading = cgi.escape(heading)
    author = cgi.escape(author)
    if post_type != 'html':
      text_content = cgi.escape(text_content)

    new_post = BlogPost(content=text_content, heading=heading, author=author)
    new_post.is_raw = post_type == 'raw'
    new_post.put()

    self.redirect('/')

class BlogPost(db.Model):
  heading = db.StringProperty(required=True)
  content = db.StringProperty(required=True)
  author = db.StringProperty()
  is_raw = db.BooleanProperty()
  date = db.DateTimeProperty(auto_now_add=True)

app = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/new', NewFormPage),
  ('/new/', NewFormPage),
  ('/new/submit', NewSubmitPage),
], debug=True)

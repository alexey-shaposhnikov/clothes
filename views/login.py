__author__ = 'admin'

from google.appengine.api import users
from tools.handler import BaseHandler


class LoginHandler(BaseHandler):
    def get(self):
        user = self.user
        if user:
            self.redirect('/')
        else:
            self.render('login')
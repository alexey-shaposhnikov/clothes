__author__ = 'admin'

from tools.handler import BaseHandler


class HomeHandler(BaseHandler):
    def get(self):
        self.render('app', user=self.user)
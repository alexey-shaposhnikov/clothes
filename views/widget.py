__author__ = 'admin'

from tools.handler import BaseHandler


class WidgetHandler(BaseHandler):

    def get(self):

        self.render('widget', {'request': 'get', 'user': self.user})

    def post(self):
        self.render('widget', {'request': 'post'})
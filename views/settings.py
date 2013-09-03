__author__ = 'admin'

from tools.handler import BaseHandler
from models.user import User


class SettingsHandler(BaseHandler):

    def get(self):

        self.render('settings', {'request': 'get', 'data': self.data, 'user': self.user})

    def post(self):
        uid = self.request.get('uid')
        settings = self.request.get('settings')
        instance_id = self.request.get('instance_id')
        self.user.uid = uid
        self.user.instance_id = instance_id
        self.user.settings = settings
        self.user.put()
        self.get()
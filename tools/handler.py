__author__ = 'admin'

try:
    import simplejson as json
except ImportError:
    import json
import os
import jinja2
import datetime
import base64
import Cookie
from google.appengine.ext import webapp
from google.appengine.api import users

from models.user import User


class BaseHandler(webapp.RequestHandler):
    logout_url = None
    login_url = None
    def render(self, name, data={}):
        JINJA_ENVIRONMENT = jinja2.Environment(
            loader=jinja2.FileSystemLoader(os.path.join(
                os.path.dirname(__file__), '../templates')),
            extensions=['jinja2.ext.autoescape'])

        template = JINJA_ENVIRONMENT.get_template(name + '.html')
        data['user'] = self.user
        data['logout_url'] = self.logout_url
        data['login_url'] = self.login_url
        self.response.write(template.render(data))

    def initialize(self, request, response):
        super(BaseHandler, self).initialize(request, response)
        user = users.get_current_user()
        if user:
            self.logout_url = users.create_logout_url('/')
            user_in_db = User.query(User.uid == user.user_id()).get()
            if user_in_db:
                user = user_in_db
            else:
                user = User(uid=user.user_id(), email=user.email(), nickname=user.nickname())
                user.put()
        else:
            self.login_url = users.create_login_url('/')
        # if 'user' in self.request.cookies:
        #     user_id = self.request.cookies.get('user')
        #     user = User.query(User.uid == user_id).get()
        #     self.data = {'uid': user.uid, 'instanceId': user.instance_id}
        #
        # if u'instance' in self.request.GET and not user:
        #     data = self.parse_user()
        #     self.set_cookie('user', data['uid'])
        #     user = User(uid=data['uid'], instance_id=data['instanceId'])
        #     self.data = data
        #     user.put()

        self.user = user

    def set_cookie(self, name, value, expires=None):
        """Set a cookie"""
        if value is None:
            value = 'deleted'
            expires = datetime.timedelta(minutes=-50000)
        jar = Cookie.SimpleCookie()
        jar[name] = value
        jar[name]['path'] = u'/'
        if expires:
            if isinstance(expires, datetime.timedelta):
                expires = datetime.datetime.now() + expires
            if isinstance(expires, datetime.datetime):
                expires = expires.strftime('%a, %d %b %Y %H:%M:%S')
            jar[name]['expires'] = expires
        _header = jar.output().split(u': ', 1)
        _header = [str(i) for i in _header]
        self.response.headers.add_header(*_header)

    def parse_user(self):
        x = self.request.GET.multi._items
        x = dict(x)
        sig, payload = x['instance'].split(u'.', 1)
        data = json.loads(self.base64_url_decode(payload))
        return data


    @staticmethod
    def base64_url_decode(data):
        data = data.encode(u'ascii')
        data += '=' * (4 - (len(data) % 4))
        return base64.urlsafe_b64decode(data)
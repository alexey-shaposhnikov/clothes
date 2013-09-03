from google.appengine.ext import ndb


class User(ndb.Model):
    uid = ndb.StringProperty(required=True)
    nickname = ndb.StringProperty()
    email = ndb.StringProperty()
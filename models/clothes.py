__author__ = 'admin'

from google.appengine.ext import ndb
from models.user import User


class Clothes(ndb.Model):
    parent = ndb.KeyProperty(kind=User, verbose_name='clothes', name='clothes')
    name = ndb.TextProperty(required=True, indexed=False)
    photo = ndb.TextProperty(indexed=False)
    created = ndb.DateTimeProperty(auto_now_add=True)


from datetime import time

__author__ = 'admin'

from google.appengine.ext import ndb
from models.user import User


class Image(ndb.Model):

    name = ndb.TextProperty(required=True, indexed=False)
    photo = ndb.TextProperty(indexed=False)
    tags = ndb.TextProperty(repeated=True, indexed=True)
    created = ndb.DateTimeProperty(auto_now_add=True)

    def to_json(self):

        return {
            "id": self.key.urlsafe(),
            "name": self.name,
            "created_at": self.created.isoformat(),
            "photo": self.photo,
            "tags": self.tags
        }


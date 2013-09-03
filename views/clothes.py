__author__ = 'admin'

from tools.handler import BaseHandler
from tools.decorators import user_required
from models.clothes import Clothes
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import blobstore
from google.appengine.ext import ndb



class ClothesHandler(BaseHandler, blobstore_handlers.BlobstoreUploadHandler):
    @user_required
    def get(self):
        upload_url = blobstore.create_upload_url('/clothes/add')
        self.render('add-clothes', upload_url=upload_url)

    @user_required
    def post(self):
        photo = self.get_uploads('photo')[0]
        name = self.request.get('name')
        photo_key = '%s' % photo.key()  # todo: change to more adequate logic
        clothes = Clothes(parent=self.user.key, name=name, photo=photo_key)
        clothes.put()
        self.redirect(self.uri_for('add_clothes'))


class ClothesShowHandler(BaseHandler):
    @user_required
    def get(self, key=None):
        clothes = ndb.Key(urlsafe=key).get()
        self.render('show-clothes', clothes=clothes)


class ClothesRemoveHandler(BaseHandler):
    @user_required
    def post(self):
        key = self.request.get('key')
        ndb.Key(urlsafe=key).delete()

        self.redirect(self.uri_for('clothes_list'))
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import blobstore
from tools.handler import BaseHandler
from tools.decorators import user_required
from models.image import Image
from dateutil import parser
import logging
import datetime
from google.appengine.ext import ndb


class ImagesAPIHandler(BaseHandler):
    def get(self):
        try:
            limit = int(self.request.get('limit'))
        except ValueError:
            limit = 20
        try:
            from_date = parser.parse(self.request.get('from', datetime.datetime.now().isoformat()))
        except:
            from_date = datetime.datetime.now()
        images = Image.query(Image.created < from_date).order(-Image.created).fetch(limit)
        self.response_json([item.to_json() for item in images])

    def post(self):
        try:
            tags = self.request.get('tags')
            if not tags or len(tags) == 0:
                tags = []
            else:
                tags = tags.strip().split(',')
                tags = [t.strip() for t in tags]
        except:
            tags = []
        item = Image(name=self.request.get('name'), tags=tags)
        item.put()
        data = item.to_json()
        data.update(upload_url=blobstore.create_upload_url('/api/images/image'))
        self.response_json(data)


class ImagesPhotoAPIHandler(BaseHandler, blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        key = self.request.get('id')
        photo = self.get_uploads('photo')[0]
        item = ndb.Key(urlsafe=key).get()
        item.photo = str(photo.key())
        if item.name == '':
            item.name = photo.filename
        item.put()
        self.response_json(item.to_json())
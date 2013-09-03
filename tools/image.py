__author__ = 'alexey'

import urllib
from google.appengine.ext import db
from tools.handler import BaseHandler
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import blobstore


class Image(BaseHandler, blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, key=None):
        resource = key
        resource = str(urllib.unquote(resource))
        blob_info = blobstore.BlobInfo.get(resource)
        if not blob_info:
            self.response.out.write(resource)
        else:
            self.response.headers['Content-Type'] = 'image/png'
            self.send_blob(blob_info)
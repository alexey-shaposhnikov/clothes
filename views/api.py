__author__ = 'admin'

from tools.handler import BaseHandler
from tools.decorators import user_required
from models.clothes import Clothes


class ClothesAPIHandler(BaseHandler):
    @user_required
    def get(self):
        clothes = Clothes.query(Clothes.parent == self.user.key).order(Clothes.created).fetch()
        self.render('home', {'user': self.user, 'clothes': clothes})
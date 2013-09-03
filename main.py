# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from views.home import HomeHandler
from views.login import LoginHandler
from views.clothes import ClothesHandler
from tools.image import Image
#from google.appengine.ext import webapp
import webapp2


os.environ[u'DJANGO_SETTINGS_MODULE'] = u'conf'


# routes = [
#     (r'/', HomeHandler),
#     (r'/login', LoginHandler),
# ]
app = webapp2.WSGIApplication([
    webapp2.Route('/', handler=HomeHandler, name='home'),
    webapp2.Route('/clothes', handler=HomeHandler, name='clothes_list'),
    webapp2.Route('/clothes/add', handler=ClothesHandler, name='add_clothes'),
    webapp2.Route('/clothes/remove', handler='views.clothes.ClothesRemoveHandler', name='clothes_remove'),
    webapp2.Route('/clothes/show/<key:.+>', handler='views.clothes.ClothesShowHandler', name='show_clothes'),
    webapp2.Route('/login', handler=LoginHandler, name='login'),
    webapp2.Route('/serve-image/<key:.+>', handler=Image, name='serve_image')
], True)
#app = webapp.WSGIApplication(routes, debug=True)


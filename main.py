# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
from views.home import HomeHandler
from tools.image import Image
import webapp2

sys.path.append(os.path.join(os.path.dirname(__file__), 'libs'))



# routes = [
#     (r'/', HomeHandler),
#     (r'/login', LoginHandler),
# ]
app = webapp2.WSGIApplication([
    webapp2.Route('/', handler=HomeHandler, name='home'),

    webapp2.Route('/api/images', handler='views.api.ImagesAPIHandler', name='images_api'),
    webapp2.Route('/api/images', handler='views.api.ImagesAPIHandler', name='images_user_api'),
    webapp2.Route('/api/images/image', handler='views.api.ImagesPhotoAPIHandler'),
    webapp2.Route('/serve-image/<key:.+>', handler=Image, name='serve_image')
], True)
#app = webapp.WSGIApplication(routes, debug=True)


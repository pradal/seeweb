from jinja2 import Markup
from pyramid.view import view_config

from seeweb.models import DBSession

from .commons import view_init


@view_config(route_name='user_view_home_default',
             renderer='templates/user/view_home.jinja2')
@view_config(route_name='user_view_home',
             renderer='templates/user/view_home.jinja2')
def view(request):
    session = DBSession()
    user, view_params = view_init(request, session, 'home')

    view_params['description'] = Markup(user.html_description())

    return view_params

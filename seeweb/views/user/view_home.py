from jinja2 import Markup
from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.views.tools import convert_rst_to_html

from .tools import view_init


@view_config(route_name='user_view_home_default',
             renderer='templates/user/view_home.jinja2')
@view_config(route_name='user_view_home',
             renderer='templates/user/view_home.jinja2')
def index(request):
    session = DBSession()
    user, view_params = view_init(request, session, 'home')

    if user.description == "":
        view_params['description'] = ""
    else:
        html = convert_rst_to_html(user.description)
        view_params['description'] = Markup(html)

    return view_params

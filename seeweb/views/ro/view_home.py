from jinja2 import Markup
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from seeweb.models import DBSession

from .commons import fetch_ro, view_init


@view_config(route_name='ro_view_home',
             renderer='templates/ro/view_home.jinja2')
@view_config(route_name='ro_view_home_default',
             renderer='templates/ro/view_home.jinja2')
def view(request):
    session = DBSession()
    uid, ro = fetch_ro(request, session)

    try:
        loc = request.route_url('ro_%s_view_home' % ro.type, uid=uid)
        return HTTPFound(location=loc)
    except KeyError:
        ro, view_params = view_init(request, session, 'home')
        view_params['description'] = Markup(ro.html_description())

        return view_params

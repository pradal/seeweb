from jinja2 import Markup
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from seeweb.models import DBSession

from .commons import view_init


@view_config(route_name='ro_view_home',
             renderer='templates/ro/view_home.jinja2')
@view_config(route_name='ro_view_home_default',
             renderer='templates/ro/view_home.jinja2')
def view(request):
    session = DBSession()
    ro, view_params = view_init(request, session, 'home')

    if ro.type == 'container':
        loc = request.route_url('ro_container_view',
                                uid=request.matchdict['uid'])
        return HTTPFound(location=loc)

    view_params['description'] = Markup(ro.html_description())

    return view_params

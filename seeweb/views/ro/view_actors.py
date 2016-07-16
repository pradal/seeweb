from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.auth import Role

from .commons import view_init


@view_config(route_name='ro_view_actors',
             renderer='templates/ro/view_actors.jinja2')
def view(request):
    session = DBSession()
    ro, view_params = view_init(request, session, 'actors')

    actors = [('user', Role.to_str(Role.edit), ro.owner)]
    for pol in ro.auth:
        actors.append(('user', Role.to_str(pol.role), pol.actor))

    view_params["actors"] = actors

    return view_params

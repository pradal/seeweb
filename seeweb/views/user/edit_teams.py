from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from seeweb.models import DBSession

from .tools import edit_common, edit_init, tabs


@view_config(route_name='user_edit_teams',
             renderer='templates/user/edit_teams.jinja2')
def view(request):
    session = DBSession()
    user, view_params = edit_init(request, session, 'teams')

    if 'default' in request.params:
        # reload default values for this user
        # actually already done
        pass
    elif 'update' in request.params:
        edit_common(request, session, user)
    else:
        pass

    return view_params

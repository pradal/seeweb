from pyramid.view import view_config

from seeweb.models import DBSession

from .tools import edit_init


@view_config(route_name='user_edit_playground',
             renderer='templates/user/edit_playground.jinja2')
def view(request):
    session = DBSession()
    user, view_params = edit_init(request, session, 'playground')

    return view_params

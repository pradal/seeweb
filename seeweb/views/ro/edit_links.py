from pyramid.view import view_config

from seeweb.models import DBSession

from .commons import edit_init


@view_config(route_name='ro_edit_links',
             renderer='templates/ro/edit_links.jinja2')
def view(request):
    session = DBSession()
    ro, view_params = edit_init(request, session, 'links')

    return view_params

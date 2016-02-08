from pyramid.view import view_config

from seeweb.models import DBSession

from .commons import edit_init


@view_config(route_name='team_edit_projects',
             renderer='templates/team/edit_projects.jinja2')
def view(request):
    session = DBSession()
    team, view_params = edit_init(request, session, 'projects')

    return view_params

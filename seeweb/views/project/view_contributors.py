from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.auth import Role

from .tools import view_init


@view_config(route_name='project_view_contributors',
             renderer='templates/project/view_contributors.jinja2')
def index(request):
    session = DBSession()
    project, view_params = view_init(request, session, 'contributors')

    members = [('user', Role.edit, project.owner)]
    for actor in project.auth:
        if actor.is_team:
            typ = 'team'
        else:
            typ = 'user'
        members.append((typ, actor.role, actor.user))

    view_params["members"] = members

    return view_params

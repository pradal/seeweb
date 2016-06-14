from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.auth import Role

from .commons import view_init


@view_config(route_name='team_view_members',
             renderer='templates/team/view_members.jinja2')
def view(request):
    session = DBSession()
    team, view_params = view_init(request, session, 'members')

    members = []
    for pol in team.auth:
        if pol.is_team:
            typ = 'team'
        else:
            typ = 'user'
        members.append((typ, Role.to_str(pol.role), pol.actor))

    view_params["members"] = members

    return view_params

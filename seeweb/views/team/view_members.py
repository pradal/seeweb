from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.auth import Role

from .commons import view_init


@view_config(route_name='team_view_members',
             renderer='templates/team/view_members.jinja2')
def index(request):
    session = DBSession()
    team, view_params = view_init(request, session, 'members')

    members = []
    for actor in team.auth:
        if actor.is_team:
            typ = 'team'
        else:
            typ = 'user'
        members.append((typ, Role.to_str(actor.role), actor.user))

    view_params["members"] = members

    return view_params

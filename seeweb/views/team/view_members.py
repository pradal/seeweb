from pyramid.view import view_config

from .tools import tabs, view_init


@view_config(route_name='team_view_members', renderer='templates/team/view_members.jinja2')
def index(request):
    team, current_uid, allow_edit = view_init(request)

    members = []
    for actor in team.auth:
        members.append((actor.role, actor.user))

    return {"team": team,
            "tabs": tabs,
            "tab": 'members',
            "allow_edit": allow_edit,
            "members": members}

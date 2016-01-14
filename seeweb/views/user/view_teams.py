from pyramid.view import view_config

from seeweb.models.auth import Role

from .tools import view_init


@view_config(route_name='user_view_teams', renderer='templates/user/view_teams.jinja2')
def index(request):
    user, current_uid, allow_edit = view_init(request)

    teams = []
    for team in user.teams:
        role = team.access_role(current_uid)
        if role != Role.denied:
            teams.append((role, team))

    return {"user": user,
            "tab": 'teams',
            "allow_edit": allow_edit,
            "teams": teams}

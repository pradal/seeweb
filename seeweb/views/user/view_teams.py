from pyramid.view import view_config

from seeweb.models.auth import Role
from seeweb.views.tools import get_current_uid

from .tools import get_user


@view_config(route_name='user_view_teams', renderer='templates/user/view_teams.jinja2')
def index(request):
    uid = request.matchdict['uid']
    user = get_user(request, uid)
    current_uid = get_current_uid(request)

    tab = 2
    teams = []

    for team in user.teams:
        role = team.access_role(current_uid)
        if role != Role.denied:
            teams.append((role, team))

    return {"user": user,
            "tab": tab,
            "allow_edit": uid == current_uid,
            "teams": teams}

from pyramid.view import view_config

from seeweb.models.auth import Role
from seeweb.views.tools import get_current_uid

from .tools import get_user


@view_config(route_name='user_home', renderer='templates/user/home.jinja2')
def index(request):
    uid = request.matchdict['uid']
    user = get_user(request, uid)
    current_uid = get_current_uid(request)

    tab = int(request.params.get("tab", 0))
    projects = []
    teams = []

    if tab == 1:
        for pjt in user.projects:
            role = pjt.access_role(current_uid)
            if role != Role.denied:
                projects.append((role, pjt))
    elif tab == 2:
        for team in user.teams:
            role = team.access_role(current_uid)
            if role != Role.denied:
                teams.append((role, team))

    return {"user": user,
            "tab": tab,
            "allow_edit": uid == current_uid,
            "projects": projects,
            "teams": teams}

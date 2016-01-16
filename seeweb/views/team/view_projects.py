from pyramid.view import view_config

from seeweb.models.auth import Role
from seeweb.views.user.tools import get_user

from .tools import tabs, view_init


@view_config(route_name='team_view_projects', renderer='templates/team/view_projects.jinja2')
def index(request):
    team, current_uid, allow_edit = view_init(request)

    projects = {}
    for actor in team.auth:
        if actor.role != Role.denied:
            user = get_user(actor.user)

            for pjt in user.projects:
                if pjt.id not in projects:
                    role = pjt.access_role(current_uid)
                    if role != Role.denied:
                        projects[pjt.id] = (role, pjt)

    return {"team": team,
            "tabs": tabs,
            "tab": 'projects',
            "allow_edit": allow_edit,
            "projects": projects.values()}

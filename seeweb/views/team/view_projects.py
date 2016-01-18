from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.auth import Role
from seeweb.models.access import get_user, project_access_role

from .tools import tabs, view_init


@view_config(route_name='team_view_projects',
             renderer='templates/team/view_projects.jinja2')
def index(request):
    session = DBSession()
    team, current_uid, allow_edit = view_init(request, session)

    projects = {}
    for actor in team.auth:
        if actor.role != Role.denied and not actor.is_team:
            user = get_user(session, actor.user)

            for pjt in user.projects:
                if pjt.id not in projects:
                    role = project_access_role(session, pjt, current_uid)
                    if role != Role.denied:
                        projects[pjt.id] = (role, pjt)

    return {"team": team,
            "tabs": tabs,
            "tab": 'projects',
            "allow_edit": allow_edit,
            "projects": projects.values()}

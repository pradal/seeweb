from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.auth import Role
from seeweb.model_access import get_user, project_access_role

from .commons import view_init


@view_config(route_name='team_view_projects',
             renderer='templates/team/view_projects.jinja2')
def view(request):
    session = DBSession()
    team, view_params = view_init(request, session, 'projects')

    projects = {}
    for actor in team.auth:
        if actor.role != Role.denied and not actor.is_team:
            user = get_user(session, actor.user)

            for pjt in user.projects:
                if pjt.id not in projects:
                    role = project_access_role(session,
                                               pjt,
                                               request.unauthenticated_userid)
                    if role != Role.denied:
                        projects[pjt.id] = (Role.to_str(role), pjt)

    view_params["projects"] = projects.values()

    return view_params

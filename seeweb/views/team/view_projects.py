from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.auth import Role
from seeweb.models.user import User

from .commons import view_init


@view_config(route_name='team_view_projects',
             renderer='templates/team/view_projects.jinja2')
def view(request):
    session = DBSession()
    team, view_params = view_init(request, session, 'projects')

    projects = {}
    for actor in team.auth:
        if actor.role != Role.denied and not actor.is_team:
            user = User.get(session, actor.user)

            for pjt in user.projects:
                if pjt.id not in projects:
                    role = pjt.access_role(session,
                                           request.unauthenticated_userid)
                    if role != Role.denied:
                        projects[pjt.id] = (Role.to_str(role), pjt)

    view_params["projects"] = projects.values()

    return view_params

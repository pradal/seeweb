from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.auth import Role

from .tools import tabs, view_init


@view_config(route_name='project_view_contributors',
             renderer='templates/project/view_contributors.jinja2')
def index(request):
    session = DBSession()
    project, current_uid, allow_edit = view_init(request, session)

    members = [('user', Role.edit, project.owner)]
    for actor in project.auth:
        if actor.is_team:
            typ = 'team'
        else:
            typ = 'user'
        members.append((typ, actor.role, actor.user))

    return {"project": project,
            "tabs": tabs,
            "tab": 'contributors',
            "allow_edit": allow_edit,
            "sections": [],
            "members": members}

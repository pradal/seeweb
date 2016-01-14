from pyramid.view import view_config

from seeweb.models.auth import Role

from .tools import view_init


@view_config(route_name='user_view_projects', renderer='templates/user/view_projects.jinja2')
def index(request):
    user, current_uid, allow_edit = view_init(request)

    projects = []
    for pjt in user.projects:
        role = pjt.access_role(current_uid)
        if role != Role.denied:
            projects.append((role, pjt))

    return {"user": user,
            "tab": 'projects',
            "allow_edit": allow_edit,
            "projects": projects}

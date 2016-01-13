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
    for pjt in user.projects:
        role = pjt.access_role(current_uid)
        if role != Role.denied:
            projects.append((role, pjt))

    return {"user": user,
            "tab": tab,
            "allow_edit": uid == current_uid,
            "projects": projects}

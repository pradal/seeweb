from pyramid.view import view_config

from seeweb.models.auth import Role
from seeweb.views.tools import get_current_uid

from .tools import get_user


@view_config(route_name='user_view_home_default', renderer='templates/user/view_home.jinja2')
@view_config(route_name='user_view_home', renderer='templates/user/view_home.jinja2')
def index(request):
    uid = request.matchdict['uid']
    user = get_user(request, uid)
    current_uid = get_current_uid(request)

    tab = 0
    projects = []
    teams = []

    return {"user": user,
            "tab": tab,
            "allow_edit": uid == current_uid}

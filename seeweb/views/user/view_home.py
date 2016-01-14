from pyramid.view import view_config

from .tools import view_init


@view_config(route_name='user_view_home_default', renderer='templates/user/view_home.jinja2')
@view_config(route_name='user_view_home', renderer='templates/user/view_home.jinja2')
def index(request):
    user, current_uid, allow_edit = view_init(request)
    tab = 0

    return {"user": user,
            "tab": tab,
            "allow_edit": allow_edit}

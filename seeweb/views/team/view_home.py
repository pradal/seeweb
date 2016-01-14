from pyramid.view import view_config

from .tools import view_init


@view_config(route_name='team_view_home', renderer='templates/team/view_home.jinja2')
@view_config(route_name='team_view_home_default', renderer='templates/team/view_home.jinja2')
def index(request):
    tid, team, current_uid, allow_edit = view_init(request)
    tab = 0

    return {"team": team,
            "tab": tab,
            "allow_edit": allow_edit}

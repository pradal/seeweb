from pyramid.view import view_config

from .tools import view_init


@view_config(route_name='team_view_projects', renderer='templates/team/view_projects.jinja2')
def index(request):
    tid, team, current_uid, allow_edit = view_init(request)
    tab = 1

    return {"team": team,
            "tab": tab,
            "allow_edit": allow_edit}

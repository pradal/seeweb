from pyramid.view import view_config

from .tools import tabs, view_init


@view_config(route_name='team_view_projects', renderer='templates/team/view_projects.jinja2')
def index(request):
    team, current_uid, allow_edit = view_init(request)

    return {"team": team,
            "tabs": tabs,
            "tab": 'projects',
            "allow_edit": allow_edit}

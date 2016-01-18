from jinja2 import Markup
from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.views.tools import convert_rst_to_html

from .tools import tabs, view_init


@view_config(route_name='team_view_home',
             renderer='templates/team/view_home.jinja2')
@view_config(route_name='team_view_home_default',
             renderer='templates/team/view_home.jinja2')
def index(request):
    session = DBSession()
    team, current_uid, allow_edit = view_init(request, session)

    if team.description == "":
        description = ""
    else:
        html = convert_rst_to_html(team.description)
        description = Markup(html)

    return {"team": team,
            "tabs": tabs,
            "tab": 'home',
            "allow_edit": allow_edit,
            "description": description}

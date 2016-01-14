from docutils.core import publish_parts
from jinja2 import Markup
from pyramid.view import view_config

from .tools import view_init


@view_config(route_name='team_view_home', renderer='templates/team/view_home.jinja2')
@view_config(route_name='team_view_home_default', renderer='templates/team/view_home.jinja2')
def index(request):
    team, current_uid, allow_edit = view_init(request)
    if team is None:
        return current_uid

    if team.description == "":
        description = ""
    else:
        html = publish_parts(team.description, writer_name='html')['html_body']
        description = Markup(html)

    return {"team": team,
            "tab": 'home',
            "allow_edit": allow_edit,
            "description": description}

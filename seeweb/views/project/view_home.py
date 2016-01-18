from jinja2 import Markup
from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.models.access import fetch_comments
from seeweb.views.tools import convert_rst_to_html

from .tools import tabs, view_init


@view_config(route_name='project_view_home_default',
             renderer='templates/project/view_home.jinja2')
@view_config(route_name='project_view_home',
             renderer='templates/project/view_home.jinja2')
def index(request):
    session = DBSession()
    request.session['last'] = request.current_route_url()
    project, allow_edit = view_init(request, session)

    if project.description == "":
        dscr = ""
    else:
        html = convert_rst_to_html(project.description)
        dscr = Markup(html)

    comments = fetch_comments(session, project.id, 2)

    return {"project": project,
            "tabs": tabs,
            "tab": 'home',
            "allow_edit": allow_edit,
            "sections": ['description',
                         'gallery',
                         'comments',
                         'extra info'],
            "short_description": dscr,
            "comments": comments}
